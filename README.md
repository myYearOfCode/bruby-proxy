# bruby-proxy
Bruby-proxy is a python api proxy server that enables an IOT homebrewing appliance to connect to the bruby heroku instance. This is used in conjunction with a local dns redirect.
![bruby-proxy terminal screengrab](https://s3.amazonaws.com/bruby/github_images/Screen+Shot+2019-05-19+at+10.03.13+PM.png)
 
 ## Demo Setup.
 Needed:
* Your homebrewing device.
* A laptop or raspberry pi acting as a wifi access point (running dnsmasq and the bruby-proxy).
* A usb wifi dongle (for sharing one connection to another access point).

 [Install dnsmasq](https://www.stevenrombauts.be/2018/01/use-dnsmasq-instead-of-etc-hosts/)
 
 Set up the laptop to share wifi from the internal wifi to an external usb wifi. 
 Config dnsmasq to point your IOT devices api url to the shared wifi ip address. The dnsmasq file will be located at `/usr/local/etc/dnsmasq.conf` if you are using a mac. Modify line 79 to look like this 
 
 ```
address=/example.com/your.shared.wifi.ip
address=/www.example.com/your.shared.wifi.ip
```

Save dnsmasq.conf, and then reset it with

```
sudo launchctl stop homebrew.mxcl.dnsmasq
sudo launchctl start homebrew.mxcl.dnsmasq
```

Now modify bruby-proxy on line 32 to point to whatever url you would like to redirect to. Run the proxy with `sudo python bruby-proxy.py 80`

At this point you can test your dns redirect with `nslookup + short targetDomain` or `dig @127.0.0.1 targetDomain` where targetDomain is the url your device is trying to connect to (and that you want to redirect)

As one last test you should connect to your new wifi point with another device and attempt to visit the target domain. You should end up with the redirected site as opposed to the original one. If this works correctly you should be able to see some debug info in the python terminal that shows the url received, and the response sent back.
