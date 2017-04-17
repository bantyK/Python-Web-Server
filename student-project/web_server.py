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
            elif self.path.endswith("/"):
                self.add_header()
                student_name = self.path.split("/")[2]
                students_with_name = db.get_students_with_name(student_name)
                output = self.get_view_for_single_student(students_with_name)
                self.wfile.write(output)
                return
            elif self.path.endswith('/student/add'):
                self.add_header()
                output = self.get_view_for_create_student()
                self.wfile.write(output)
                return
            elif self.path.endswith('/edit'):
                self.add_header()
                student_name = self.path.split("/")[2]
                print student_name
                student = db.get_students_with_name(student_name)
                output = self.get_view_for_edit(student[0])
                self.wfile.write(output)
                return
            elif self.path.endswith("/delete"):
                self.add_header()
                student_name = self.path.split("/")[2]
                student = db.get_students_with_name(student_name)
                output = self.get_view_for_delete(student[0])
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

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    student_name = fields.get("name")[0]
                    student_address = fields.get("address")[0]
                    student_city = fields.get("city")[0]
                    student_stream = fields.get("stream")[0]
                    student_gender = fields.get("gender")[0]

                    print(student_name, student_address, student_city, student_stream, student_gender)
                    new_student = Student(name=student_name, address=student_address, city=student_city,
                                          stream=student_stream, gender=student_gender)

                student_name = self.path.split("/")[2]
                db.updateStudentData(student_name, new_student)
                self.add_redirect_headers()

            if self.path.endswith("/delete"):
                student_name = self.path.split("/")[2]
                db.deleteStudent(student_name)
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
        output += "<h1><a href = '/student/add'>Add a new student</a></h1>"
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
            output += '<p><a href="/student/%s/edit"> Edit  </a><a href="/student/%s/delete"> Delete</a></p>' % (
                student.name, student.name)

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

    def get_view_for_edit(self, student):
        output = "<html><body>"
        output += "<form method='POST' enctype=multipart/form-data action = /student/%s/edit>" % student.name
        output += "<p>Name  : <input type='text' name = 'name' placeholder = '%s'></p>" % student.name
        output += "<p>Address : <input type='text' name = 'address' placeholder = '%s'></p>" % student.address
        output += "<p>City : <input type='text' name = 'city' placeholder = '%s'></p>" % student.city
        output += "<p>Stream : <input type='text' name = 'stream' placeholder = '%s'></p>" % student.stream
        output += "<p>Gender : <input type='text' name = 'gender' placeholder = '%s'></p>" % student.gender
        output += "<p><input type='submit' value = 'Update'></p>"
        output += "</form>"
        output += "</body></html>"
        return output

    def get_view_for_delete(self, student):
        output = "<html><body>"
        output += "<h1> Are you sure you want to delete %s from database?" % student.name
        output += "<form method='POST' enctype=multipart/form-data action = /student/%s/delete>" % student.name
        output += "<input type='submit' value = 'Delete'>"
        output += "</form>"
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
