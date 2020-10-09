import os
import sys
from datetime import datetime, timedelta
from azure.eventhub import EventHubConsumerClient
time = datetime.utcnow()
DeviceName = sys.argv[1]
if sys.argv[2] == 'start':
    positioning = "1"
elif sys.argv[2] == 'end':
    positioning = "@latest"
elif sys.argv[2] =='time':
    noOfDays = "time"
    
    if(noOfDays == "time"):
        userInput = input("Enter no. of days: ")
        time = datetime.utcnow()
        positioning = time - timedelta(days = int(userInput))

else: 
    positioning = "1"


CONNECTION_STR = 'Endpoint=sb://iothub-ns-hypernet-r-3032872-8d1cc0e2e1.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=3sx6J+Ii9WJWPJM8BvN/I2geZGS/GX9tv5ucUrFawcw=;EntityPath=hypernet-reliance-iothub'
EVENTHUB_NAME = 'hypernet-reliance-iothub'

print(time)
file = open(DeviceName + ".csv","w")
file.write("Device ID, Firmware Version, GPS Fix Status, Signal Strength, MCUSR Value, Last Error Cause, Reset Counter, Current Voltage, Bit Error Rate, Timestamp, Speed, Latitude, Longitude, Sharp Acceleration Flag, Sharp Deceleration Flag, Sharp Turning Flag, Main Supply Status, Real Time Packet, Environment Temp, , ,Time\n")
file.close()


def on_event(partition_context, event):

  
    #print("Received messages from eventhub: {}.".format(event.body_as_str(encoding='UTF-8'),partition_context.partition_id))
 
    k = event.body_as_str(encoding='UTF-8')
    enqueTime = partition_context.last_enqueued_event_properties
    
    if k.find(DeviceName) == -1:
        a = 0
    else:
        #filteredEnqueTime =   enqueTime['enqueued_time'] 
        s = k.replace('{"id":', '').replace('"', '').replace('ts:', '').replace('d:', '').replace('t:', '').replace('sp', '').replace('la', '').replace('lon:', '').replace('saf:','').replace('sdf:','').replace('stf:','').replace('mss:','').replace('rtp:','').replace('evTemp:','').replace('stf:','').replace('mss:', '').replace('rtp:','').replace('evTemp:','').replace('type: 3','').replace('module: 1','').replace('customer: 1}','')
        file = open(DeviceName + ".csv","a")
        file.write(s  + "\n")
        file.close()
        print(k)
        #print(enqueTime['enqueued_time'])
        
        
      
 
 
def on_partition_initialize(partition_context):

    print("Preparing: {} ".format(partition_context.partition_id))


def on_partition_close(partition_context, reason):

    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


def on_error(partition_context, error):

    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


if __name__ == '__main__':
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group='$Default',
        eventhub_name=EVENTHUB_NAME,
    )

    try:
        with consumer_client:
            consumer_client.receive(
                on_event=on_event,
                on_partition_initialize=on_partition_initialize,
                on_partition_close=on_partition_close,
                on_error=on_error,
                track_last_enqueued_event_properties=True,
                starting_position=positioning, 
            )
    except KeyboardInterrupt:
        print('Stopped receiving.')
