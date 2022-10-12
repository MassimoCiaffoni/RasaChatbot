from pyngrok import ngrok

http_tunnel = ngrok.connect(5005)
print(http_tunnel)