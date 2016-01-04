sudo apt-get -y update
sudo apt-get -y install uuid git rabbitmq-server python-pika python-pycurl python-pip
sudo pip install boto3
git clone http://github.com/wilsonc101/R.Pi_Rover ~/vehicle-sim
mv ~/vehicle-sim/simulator/ttyvehicle/simdata_uk.py ~/vehicle-sim/simulator/ttyvehicle/sim_data.py
mkdir ~/vehicle-sim/simulator/ttyvehicle/logs
echo $(uuid | sed 's/-.*//') > ~/id.txt
echo "vehicleID:"$(cat ~/id.txt)
nohup python /home/ubuntu/vehicle-sim/simulator/ttyvehicle/pi_rover -i $(cat ~/id.txt) -l /home/ubuntu/vehicle-sim/simulator/ttyvehicle/logs/rover.log -c /home/ubuntu/vehicle-sim/simulator/ttyvehicle/config/pi_rover.cfg > std.out 2> std.err < /dev/null &
nohup python /home/ubuntu/vehicle-sim/simulator/ttyvehicle/adaptors/aws_sqs/sqs_adaptor -v $(cat ~/id.txt) -i <SQS_ID> -k <SQS_KEY> -l /home/ubuntu/vehicle-sim/simulator/ttyvehicle/logs/sqs_adaptor.log -c /home/ubuntu/vehicle-sim/simulator/ttyvehicle/adaptors/aws_sqs/config/sqs_adaptor.cfg > std.out 2> std.err < /dev/null &
