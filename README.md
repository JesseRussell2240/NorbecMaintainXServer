# Tankfarm-Reporting


test

TODO
1. Fix failed to send message on a 201 status because that actually indicated success
2. Fix bug with random crashing by adding try catches to the transmit and tag reading
3. add remaining tank farm sensors Level, pressure and tempature
4. Explore self genorating possibility with API?
5. see vorne scoreboard "WSdata" for possible import stratagy?

6. Test how fast reporting can occure and check pressure between storage tank and day tank
7. List tags in appropriate manner
8. Create better naming convention in maintain X
9. Determin conversion for tanks to Liters?
10. 


AUTO START ON REBOOT.
1. crontab -e
2. 1(nano)
3. Add this to the end odf the file -   @reboot /usr/bin/python3 /home/rpi/Desktop/Tankfarm-Reporting-main/main.py 

