import processing.net.*;
import controlP5.*;


// General use vars
int i, w, c, d, ds, b, ka, REMOTE_PORT;
int gim_x_center, gim_y_center;
String REMOTE_IP, con_test;

// Network client
Client net_c;

// Servo vars
int DIR_MIN_ANGLE, DIR_MAX_ANGLE, DIR_NEU_ANGLE, DIR_RAMPING, dir_out_angle;
int ACC_MIN_ANGLE, ACC_MAX_ANGLE, ACC_NEU_ANGLE, ACC_RAMPING, acc_out_angle;
int BRK_ON_ANGLE, BRK_OFF_ANGLE, BRK_NEU_ANGLE, BRK_RAMPING, brk_out_angle;
int GIM_Y_MIN_ANGLE, GIM_Y_MAX_ANGLE, GIM_Y_NEU_ANGLE, GIM_Y_RAMPING, gim_y_out_angle;
int GIM_X_MIN_ANGLE, GIM_X_MAX_ANGLE, GIM_X_NEU_ANGLE, GIM_X_RAMPING, gim_x_out_angle;

// Interface objects - ControlP5
ControlP5 obj_cp5;
Slider2D sld2_cam;
Slider sld_acc, sld_dir;
Textarea obj_disc_text;
Textfield obj_in_remote_ip, obj_in_remote_port;
Button obj_btn_connect, obj_btn_stop;
Group grp_cam, grp_ctrl;



void setup() {
  size(600,280);
  obj_cp5 = new ControlP5(this);


  // Define default network connection 
  REMOTE_IP = "192.168.1.50";  
  REMOTE_PORT = 5005;
  
  net_c = new Client(this, REMOTE_IP, REMOTE_PORT);
  con_test = "pass";

  // Servo limits - Direction/Steering
  DIR_MIN_ANGLE = 256;
  DIR_MAX_ANGLE = 470;
  DIR_NEU_ANGLE = 352;
  DIR_RAMPING   = 12;

  // Servo limits - Accel/Throttle
  ACC_MIN_ANGLE = 150;
  ACC_MAX_ANGLE = 600;
  ACC_NEU_ANGLE = 352;
  ACC_RAMPING   = 16;

  // Servo limits - Brake
  BRK_ON_ANGLE = 350;
  BRK_OFF_ANGLE = 410;
  BRK_NEU_ANGLE = 410;
  BRK_RAMPING   = 1;

  // Servo limits - Gimbal Y-axis
//  GIM_Y_MIN_ANGLE = 290;
  GIM_Y_MIN_ANGLE = 100;
  GIM_Y_MAX_ANGLE = 640;
  GIM_Y_NEU_ANGLE = 580;
  GIM_Y_RAMPING = 12;

  // Servo limits - Gimbal X-axis  
  GIM_X_MIN_ANGLE = 660;
  GIM_X_MAX_ANGLE = 130;
  GIM_X_NEU_ANGLE = 377;
  GIM_X_RAMPING = 12;
   
  
  // Servo default positions
  dir_out_angle = DIR_NEU_ANGLE;
  acc_out_angle = ACC_NEU_ANGLE;
  brk_out_angle = BRK_NEU_ANGLE;
  gim_y_out_angle = GIM_Y_NEU_ANGLE;
  gim_x_out_angle = GIM_X_NEU_ANGLE;
  
  // Slider center position (additional to min value)
  //gim_y_center = (GIM_Y_MAX_ANGLE - GIM_Y_MIN_ANGLE) / 2;
  //gim_x_center = (GIM_X_MAX_ANGLE - GIM_X_MIN_ANGLE) / 2;
  //gim_y_center = GIM_Y_NEU_ANGLE - 270;  
  gim_y_center = GIM_Y_NEU_ANGLE - GIM_Y_MIN_ANGLE;
  gim_x_center = GIM_X_NEU_ANGLE - GIM_X_MIN_ANGLE;
  
  
  // Reset loop counter
  i = 0;

  // Build interface
  //CONNECTED INTERFACE
  grp_cam = obj_cp5.addGroup("camera")
     .setPosition(420,40)
     .setWidth(120)
     .setBackgroundHeight(200)
     .setBackgroundColor(color(255,50))
     ;

  grp_ctrl = obj_cp5.addGroup("controls")
     .setPosition(60,40)
     .setWidth(350)
     .setBackgroundHeight(200)
     .setBackgroundColor(color(255,50))
     ;

  sld2_cam = obj_cp5.addSlider2D("sld2_cam")
     .setPosition(10,30)
     .setSize(100,100)
     
     //.setArrayValue(new float[] {GIM_Y_NEU_ANGLE, GIM_X_NEU_ANGLE})
     //.setArrayValue(GIM_Y_NEU_ANGLE, GIM_X_NEU_ANGLE)
     .setGroup(grp_cam)
     .setCaptionLabel("gimbal")
     .setMinY(GIM_Y_MIN_ANGLE)
     .setMaxY(GIM_Y_MAX_ANGLE)
     .setMinX(GIM_X_MIN_ANGLE)
     .setMaxX(GIM_X_MAX_ANGLE)
     .setArrayValue(new float[] {gim_x_center,gim_y_center})
     ;

  obj_cp5.addButton("btn_center_cam")
     .setPosition(10,155)
     .setSize(100,20)
     .setValue(0)
     .setGroup(grp_cam)
     .setCaptionLabel("center")
     ;

  sld_acc = obj_cp5.addSlider("sld_accl")
     .setPosition(40,10)
     .setSize(30,170)
     .setRange(ACC_MIN_ANGLE,ACC_MAX_ANGLE)
     .setValue(acc_out_angle)
     .setSliderMode(Slider.FLEXIBLE)
     .setGroup(grp_ctrl)
     .setCaptionLabel("accl")
     ;
      
  sld_dir = obj_cp5.addSlider("sld_dir")
     .setPosition(115,40)
     .setSize(200,30)
     .setRange(DIR_MAX_ANGLE,DIR_MIN_ANGLE)
     .setValue(dir_out_angle)
     .setSliderMode(Slider.FLEXIBLE)
     .setGroup(grp_ctrl)
     .setCaptionLabel("dir")
     ;
      
   obj_btn_stop = obj_cp5.addButton("btn_stop")
     .setPosition(165,115)
     .setSize(100,40)
     .setValue(0)
     .setGroup(grp_ctrl)
     .setCaptionLabel("STOP")
     .setColorActive(#FF0000)
     .setColorForeground(#BB0000)
     .setColorBackground(#550000)
     ;


   // DISCONNECTED INTERFACE      
   obj_disc_text = obj_cp5.addTextarea("obj_disc_text")
     .setPosition(230,120)
     .setSize(125,20)
     .setFont(createFont("arial",12))
     .setLineHeight(14)
     .setColor(#FFFFFF)
     .setColorBackground(#990000)
     .setColorForeground(#990000)
     .setText(" DISCONNECTED")
     ;
     
   obj_in_remote_ip = obj_cp5.addTextfield("in_remote_ip")
     .setPosition(140,190)
     .setSize(130,20)
     .setFont(createFont("arial",12))
     .setFocus(true)
     .setColor(#FFFFFF)
     .setValue(REMOTE_IP)
     .setCaptionLabel("remote IP")
     ;
     
   obj_in_remote_port = obj_cp5.addTextfield("in_remote_port")
     .setPosition(280,190)
     .setSize(65,20)
     .setFont(createFont("arial",12))
     .setFocus(false)
     .setColor(#FFFFFF)
     .setValue(str(REMOTE_PORT))
     .setCaptionLabel("remote port")
     ;     
     
   obj_btn_connect = obj_cp5.addButton("btn_connect")
     .setPosition(370,190)
     .setSize(55,20)
     .setValue(0)
     .setCaptionLabel("connect")
     ;
  
  smooth();
  background(140);
    
}



void draw() {

  if (d == 1){
    thread_pause(600);
    d = 0;
  }
  
  update_interface();  

  // Check connection
 try {
    if(net_c.ip() == "" ){};
  } catch (NullPointerException e) {
    con_test = "fail";
  }
  
  if(con_test == "fail"){
    net_c = new Client(this, REMOTE_IP, REMOTE_PORT);
    con_test = "pass";
     try {
       if(net_c.ip() == "" ){};
     } catch (NullPointerException e) {
      con_test = "fail";
     }
  }
    
  //First run output
  if(i == 0){
    i++;
      if(con_test == "pass"){
        net_write();
      }
  }
    
  
  //Hide controls if disconnected, draw if OK
  if(con_test == "pass"){
     grp_cam.setOpen(true); 
     grp_ctrl.setOpen(true);
     obj_disc_text.setVisible(false);
     obj_in_remote_ip.setVisible(false);
     obj_in_remote_port.setVisible(false);
     obj_btn_connect.setVisible(false);
     background(140);
  } else if(con_test == "fail"){
     grp_cam.setOpen(false); 
     grp_ctrl.setOpen(false);
     obj_disc_text.setVisible(true);
     obj_in_remote_ip.setVisible(true);
     obj_in_remote_port.setVisible(true);
     obj_btn_connect.setVisible(true);
     background(#990000);
  }

  
  // KEY STROBING  
  /*  Key mappings:
      z  =  Direction - LEFT   (auto-center)
      x  =  Direction - RIGHT  (auto-center)
      q  =  Direction - LEFT   (hold)
      w  =  Direction - RIGHT  (hold)
      k  =  Accel     - UP
      m  =  Accel     - DOWN
      space = All stop/reset
      b  =  Release Brake
  */

  if(keyPressed == true && con_test == "pass"){
    if(key == 'k' || key == 'm'  || key == 'q'  || key == 'w') thread_pause(90);       // Debounce/Slow keyrepeats

    if(keyPressed == true && key == 'z' && dir_out_angle < DIR_MAX_ANGLE){
        dir_out_angle = dir_out_angle + DIR_RAMPING;
        ds = 0;
        
    } else if(keyPressed == true && key == 'x' && dir_out_angle > DIR_MIN_ANGLE){
        dir_out_angle = dir_out_angle - DIR_RAMPING;
        ds = 0;

    } else if(keyPressed == true && key == 'q' && dir_out_angle < DIR_MAX_ANGLE){
        dir_out_angle = dir_out_angle + DIR_RAMPING;
        ds = 1;        
        
    } else if(keyPressed == true && key == 'w' && dir_out_angle > DIR_MIN_ANGLE){
        dir_out_angle = dir_out_angle - DIR_RAMPING;
        ds = 1;
        
    } else if(keyPressed == true && key == 'k' && acc_out_angle < ACC_MAX_ANGLE){
        acc_out_angle = acc_out_angle + ACC_RAMPING;  
        if(acc_out_angle == ACC_NEU_ANGLE) d = 1;
        brk_out_angle = BRK_OFF_ANGLE;
        
    } else if(keyPressed == true && key == 'm' && acc_out_angle > ACC_MIN_ANGLE){
        acc_out_angle = acc_out_angle - ACC_RAMPING;  
        if(acc_out_angle == ACC_NEU_ANGLE) d = 1;
        brk_out_angle = BRK_OFF_ANGLE;
      
    } else if(keyPressed == true && key == ' '){
        acc_out_angle = ACC_NEU_ANGLE;
        brk_out_angle = BRK_ON_ANGLE;
        ds = 0;
        b = 1;     
    } else if(keyPressed == true && key == 'b'){
        brk_out_angle = BRK_OFF_ANGLE;
    }

    net_write();
    update_interface();
      
  } else {    // Reset to neutral values

      if(dir_out_angle != DIR_NEU_ANGLE){
        if(ds == 0){ 
           dir_out_angle = DIR_NEU_ANGLE;
           net_write();
           update_interface();
        }
      }
  }  
  // KEY STROBING -- END --
  
  // KEEP ALIVE
  // Repeat last output as keep alive every 100 cycles
  if(ka == 100){
    ka = 0;
    net_write();
  } else {
    ka = ka +1;
  }
  // KEEP ALIVE -- END --
  
}


void update_interface(){
  if (brk_out_angle == BRK_ON_ANGLE){
      obj_btn_stop.setColorActive(#FF0000);
      obj_btn_stop.setColorForeground(#FF0000);
      obj_btn_stop.setColorBackground(#FF0000);
  } else {
      obj_btn_stop.setColorActive(#FF0000);
      obj_btn_stop.setColorForeground(#BB0000);
      obj_btn_stop.setColorBackground(#550000);
  }

  sld_acc.setValue(acc_out_angle);
  sld_dir.setValue(dir_out_angle);
}

void net_write() {
  // Network Output
  net_c.write("0." + int(dir_out_angle) + ",8." + int(acc_out_angle) + ",4." + int(brk_out_angle) + ",12." + int(gim_x_out_angle)  + ",13." + int(gim_y_out_angle));
  thread_pause(10);
}

void thread_pause(int ms){
  try
  {    
    Thread.sleep(ms);
  }
  catch(Exception e){}
}

public void sld2_cam() {
  gim_x_out_angle = int(sld2_cam.getArrayValue()[0]);
  gim_y_out_angle = int(sld2_cam.getArrayValue()[1]);
  net_write();
}

/* NOT USED
public void sld_acc() {
  acc_out_angle = int(sld_acc.getValue());
  net_write();
}
public void sld_dir() {
  dir_out_angle = int(sld_dir.getValue());
  net_write();
}
*/

public void btn_center_cam() {
  sld2_cam.setArrayValue(new float[] {gim_x_center,gim_y_center});
}

public void btn_stop() {
  dir_out_angle = DIR_NEU_ANGLE;
  acc_out_angle = ACC_NEU_ANGLE;

  if (brk_out_angle == BRK_ON_ANGLE){
    brk_out_angle = BRK_OFF_ANGLE;
  } else {
    brk_out_angle = BRK_ON_ANGLE;
  }
  net_write();
}

public void btn_connect() {
  REMOTE_IP = obj_in_remote_ip.getText();
  REMOTE_PORT = int(obj_in_remote_port.getText());
}
