from flask import Flask, render_template, request
from visitor_manager import VisitorManager
# from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

visitor_manager = VisitorManager()


@app.route('/', methods=['POST', 'GET'])
def get_ip():
    visitor_ip = visitor_manager.get_ip()  # get client IP
    if not visitor_manager.ip_visited(visitor_ip): # If client visiting first time get Name and list new visitor
        if request.method == 'POST':
            visitor_manager.list_new_visitor(visitor_ip)
            return render_template("index.html", visitor_ip=visitor_manager.new_visitor['visitor_ip'],
                                   name=visitor_manager.new_visitor['name'],
                                   ip_owner=visitor_manager.new_visitor['ip_owner'],
                                   new_visitor=visitor_manager.new_visitor)
    else:  #if client already visited render page with visitor details
        for vst in visitor_manager.visitor_list['visitors']:
            if vst['visitor_ip'] == visitor_ip:
                name = vst['name']
                return render_template("index.html", visitor_ip=visitor_ip, name=name, new_visitor=None)
    
    return render_template("index.html", visitor_ip="", name="", new_visitor=None)


@app.route("/all_visitors", methods=['GET'])
def all_visitors(): # Render page with all visitors list
    return render_template("all_visitors.html", visitors=visitor_manager.visitor_list['visitors'])


if __name__ == "__main__":
    app.run(debug=True, port=5002)

