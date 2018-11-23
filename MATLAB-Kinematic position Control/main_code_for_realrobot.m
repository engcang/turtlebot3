rosshutdown
clc
clear 
close all

rosinit('192.168.0.10'); % type your robot's IP
tbot = turtlebot;
resetOdometry(tbot); % Reset robot's Odometry

robot = rospublisher('/cmd_vel');
velmsg = rosmessage(robot);

odom = rossubscriber('/odom');
odomdata = receive(odom,3); % wait up to 3 seconds, returning error if got timeout
pose = odomdata.Pose.Pose;
Ax = pose.Position.X;
Ay = pose.Position.Y;
quat = pose.Orientation;
angles = quat2eul([quat.W quat.X quat.Y quat.Z]); % transformation from quaternion to euler angles
theta = angles(1); %robot's heading angle
    
%% System Parameters
K1=2;
K2=2; %gain


xt=1;
yt=1; %xt= target.x, yt = target.y
rho=sqrt((xt-Ax)^2+(yt-Ay)^2);

while 1
if rho >=0.02
    rho=sqrt((xt-Ax)^2+(yt-Ay)^2);
    psi=atan2(yt-Ay,xt-Ax);
    phi=theta-psi;

    if phi > pi
        phi = phi - 2*pi;
    end
    if phi < -pi
        phi = phi + 2*pi;
    end % for robot angle range

%disp([theta*180/pi psi*180/pi phi*180/pi]);

    velmsg.Linear.X = K1*rho*cos(phi);
    velmsg.Angular.Z = -K1*sin(phi)*cos(phi)-K2*phi;

    if velmsg.Linear.X >= 0.22
        velmsg.Linear.X=0.22;
    end
    if velmsg.Linear.X <= -0.22
        velmsg.Linear.X=-0.22;
    end
    if velmsg.Angular.Z >= 2
        velmsg.Linear.Z=2;
    end
    if velmsg.Angular.Z <= -2
        velmsg.Angular.Z=-2;
    end % saturation for robot velocity maximum range
    
    send(robot,velmsg); %sending input into real robot via ROS
    
    odomdata = receive(odom,3);
    pose = odomdata.Pose.Pose;
    Ax = pose.Position.X;
    Ay = pose.Position.Y;
    quat = pose.Orientation;
    angles = quat2eul([quat.W quat.X quat.Y quat.Z]);
    theta = angles(1);  %update robot's position information
else
    velmsg.Linear.X=0;
    velmsg.Angular.Z=0;
    send(robot,velmsg);
    break;
end
end
