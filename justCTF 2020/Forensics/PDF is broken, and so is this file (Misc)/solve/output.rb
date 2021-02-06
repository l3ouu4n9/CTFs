require 'json'
require 'cgi'
require 'socket'
=begin
%PDF-1.5
% `file` sometimes lies
% and `readelf -p .note` might be useful later
9999 0 obj
/Length 1680
stream
=end
port = 8080
if ARGV.length > 0 then
  port = ARGV[0].to_i
html=DATA.read().encode('UTF-8', 'binary', :invalid => :replace, :undef => :replace).split(/<\/html>/)[0]+"</html>\n"
v=TCPServer.new('',port)
print "Server running at http://localhost:#{port}/\nTo listen on a different port, re-run with the desired port as a command-line argument.\n\n"
loop do
  s=v.accept
  ip = Socket.unpack_sockaddr_in(s.getpeername)[1]
  print "Got a connection from #{ip}\n"
  request=s.gets
  if request != nil then
    request = request.split(' ')
  end
  if request == nil or request.length < 2 or request[0].upcase != "GET" then
    s.print "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
    s.close
    next
  end
  req_filename = CGI.unescape(request[1].sub(/^\//,""))
  print "#{ip} GET /#{req_filename}\n"
  if req_filename == "favicon.ico" then
      s.print "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
      s.close
      next
  elsif req_filename.downcase.end_with? ".zip" then
    c="application/zip"
    d=File.open(__FILE__).read
    n=File.size(__FILE__)
  else
    c="text/html"
    d=html
    n=html.length
  end
  begin
    s.print "HTTP/1.1 200 OK\r\nContent-Type: #{c}\r\nContent-Length: #{n}\r\nConnection: close\r\n\r\n"+d
    s.close
  rescue Errno::EPIPE
    print "Connection from #{ip} closed; broken pipe\n"
  end
__END__
<html>
  <head>
    <title>A PDF that is also a Ruby Script?</title>
  </head>
  <body>
    <center>
      <a href="/flag.zip"><h1>Download</h1></a>
    </center>
    <!-- this is not the flag -->
  </body>
</html>
