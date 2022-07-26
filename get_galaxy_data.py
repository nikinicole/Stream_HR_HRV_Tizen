# -*- coding: utf-8 -*-
"""
main 


"""

import asyncio
import websockets


from functions import *

if __name__ == '__main__':
    
    

    port = 8088   
    print("Starting server on {}...".format(get_ip()) + 'oon port:' + str(port))
    
    
    loop = asyncio.get_event_loop()

    


    
    watch_server = loop.run_until_complete(websockets.serve(watch, '0.0.0.0', port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nBye bye...")

    watch_server.close()
    loop.run_until_complete(watch_server.wait_closed())
    
    
