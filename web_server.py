from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import database_operations as db
import cgi
from database_setup import Student


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/students"):
                self.add_header()
                students = db.get_all_students()
                output = self.get_view_for_student_list(students)
                self.wfile.write(output)
                return
            if self.path.endswith("/"):
                self.add_header()
                student_name = self.path.split("/")[2]
                students_with_name = db.get_students_with_name(student_name)
                output = self.get_view_for_single_student(students_with_name)
                self.wfile.write(output)
                return
            if self.path.endswith('/student/add'):
                self.add_header()
                output = self.get_view_for_create_student()
                self.wfile.write(output)
                return

        except Exception as e:
            print e

    def do_POST(self):
        try:
            if self.path.endswith('/student/add'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    student_name = fields.get("name")[0]
                    student_address = fields.get("address")[0]
                    student_city = fields.get("city")[0]
                    student_stream = fields.get("stream")[0]
                    student_gender = fields.get("gender")[0]

                    new_student = Student(name=student_name, address=student_address, city=student_city,
                                          stream=student_stream, gender=student_gender)
                    db.add_into_database(new_student)

                    self.add_redirect_headers()

        except Exception as e:
            print e

    def add_redirect_headers(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/students')
        self.end_headers()

    def add_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def get_view_for_student_list(self, students):
        output = "<html><body>"
        for student in students:
            output += '<h1> <a href="/student/%s/"> %s </a></h1>' % (student.name, student.name)
        output += "</body></html>"
        return output

    def get_view_for_single_student(self, students):
        output = "<html><body>"
        for student in students:
            output += '<p>Name : %s </p>' % student.name
            output += '<p>Address : %s </p>' % student.address
            output += '<p>City :  %s </p>' % student.city
            output += '<p>Stream :  %s </p>' % student.stream
            output += '<p>Gender :  %s </p>' % student.gender
        output += "</body></html>"
        return output

    def get_view_for_create_student(self):
        output = "<html><body>"
        output += '''
                    <h1> Add A New Student</h1>
                    <form method = 'POST' enctype = 'multipart/form-data' action = '/student/add'>
                        <p>Name  : <input type='text' name = 'name'></p>
                        <p>Address : <input type='text' name = 'address'></p>
                        <p>City : <input type='text' name = 'city'></p>
                        <p>Stream : <input type='text' name = 'stream'></p>
                        <p>Gender : <input type='text' name = 'gender'></p>
                        <p><input type='submit' name = 'Add'></p>
                    </form>
                  '''
        output += "</body></html>"
        return output


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print 'Web server running...'
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()
