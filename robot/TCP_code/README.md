# SETUP
Have the following files in the programs folder of the Kawasaki robot arm:
-TCP_server_test.as
-TCP_server_open.as
-TCP_server_send.as
-TCP_server_recv.as
-TCP_server_clos.as
-Run_message.as

Add to the global real variables list the following variables and give them the defined values:
socket_ID		-1
TCP_listen_act	0

# LOOK OUT
When you create the files in the KIDE you need to manually add the header variables for the different functions.

# RUN ON ROBOT
To use the TCP communication run the TCP_srver_test.as script.

# RUN ON PC
Use the TCP_Communication_test_pc_client.py file as an example this will be more simplefied later.