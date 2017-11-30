from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


#Add the CURD functionality
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem



#Create the session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<a href ='/restaurants/new' >Make a new restaurant here </a> "
                output += "</br></br></br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href ='#' >Edit </a> "
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "</br>"
                #output += "</br></br></br>"
                output += "</body></html>"
                self.wfile.write(output)

                print 'INA',output
                return
                
                
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                #output += "<a href ='#' >Make a new restaurant here </a> "
                #output += "</br></br></br></br>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Make a new restaurant here</h2><input name="message" type="text" ><input type="submit" value="Create a new restaurant here"> </form>'''

                self.wfile.write(output)
                print 'INB',output
                return
                    
        except IOError:
                print 'IOError'



        
                
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
