from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD operations from data_population
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype ='multipart/form-data' action ='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name= 'newRestaurantName' type='text'>"
                    output += "<input type = 'submit' value='Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output.encode('utf-8'))

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += "Are you sure you want to delete %s ?" % myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype ='multipart/form-data' action ='/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<button type='submit'>Delete</button>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output.encode('utf-8'))

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a New Restautant Here</a>"

                items = session.query(Restaurant).all()
                for item in items:
                    output += "<p> %s </p>" % item.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % item.id
                    output += "<br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % item.id
                    output += "<br>"
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output =""
                output += "<html><body>"
                output += "<h2>Make a New Restaurant</h2>"
                output += "<form method='POST' enctype ='multipart/form-data' action ='/restaurants/new'><input name ='newRestaurantName' type ='text'><input type='submit' value ='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                return

        except IOError:
            self.send_error(404,'File Not Found %s' %self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary']=bytes(pdict['boundary'],"utf-8")
                if ctype=='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0].decode('utf-8')
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type',"text/html")
                        self.send_header('Location',"/restaurants")
                        self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary']=bytes(pdict['boundary'],"utf-8")
                if ctype=='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        session.delete(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type',"text/html")
                        self.send_header('Location',"/restaurants")
                        self.end_headers()

            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary']=bytes(pdict['boundary'],"utf-8")
                if ctype=='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    restaurant_add = Restaurant(name=messagecontent[0].decode('utf-8'))
                    session.add(restaurant_add)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type',"text/html")
                    self.send_header('Location',"/restaurants")
                    self.end_headers()

        except:
            print("some error")

def main():
    try:
        port = 8080
        server = HTTPServer(("",port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

if __name__ =="__main__":
    main()
