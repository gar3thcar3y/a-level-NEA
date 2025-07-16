#include "esp_camera.h"
#include "Arduino.h"
#include "WiFi.h"
#include <WiFiUdp.h>
#include <base64.h>
using namespace std;

// Pin definition for CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22


camera_fb_t * fb = NULL;
const char* ssid = "TNCAP6684C5";
const char* password = "1B4FD47983";
WiFiClient client;
WiFiUDP Udp;
const int shapex = 100;
const int shapey = 100;

String transmition_data;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  //wifi and connections set up
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
  Serial.print("WiFi connected with IP:");
  Serial.println(WiFi.localIP());
   if(!client.connect(IPAddress(192,168,1,112), 10000)){      // <<<<<< fixed
    Serial.println("Connection to host failed");
    delay(1000);
    return;
  }
  Serial.println("\nConnected!");
  Serial.println(WiFi.localIP());

  //start up cam
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // Init Camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
  Serial.println(client.readStringUntil('\n'));
  client.println("cam 1");
}

int skip_num = 0;


float prev_total = 0;
float total = 0;


void loop() {
  // put your main code here, to run repeatedly:
  if(skip_num >= 5){
    skip_num = 0;
    total = 0;
    camera_fb_t *fb = esp_camera_fb_get();
    for (int y = 0; y < fb->height; y++) {
        for (int x = 0; x < fb->width; x++) {
            uint8_t *p = fb->buf + y * fb->width * 3 + x * 3;
            total += p[0] + p[1] + p[2]; // Red channel
        }
    }
    esp_camera_fb_return(fb);
    Serial.println(prev_total);
    Serial.println(total);


    if(((prev_total - total) > 50000000) or ((prev_total - total) < -50000000)){


      Serial.println("motion detected");
      client.print("motiondetected");
      Serial.println(client.readStringUntil('\n'));


      int loop = 0;
      while(loop < 20){
        camera_fb_t *fb = esp_camera_fb_get();
        if(!fb) {
            Serial.println("Camera capture failed");
        } else {
            const char *data = (const char *)fb->buf;
            Serial.println("Camera capture successful!");
            Serial.println(fb->width);
            Serial.println(fb->height);
            client.write(data, fb->len);
        }


        esp_camera_fb_return(fb);
        Serial.println("data sent");
        delay(500);
        loop += 1;


        }
      }


    prev_total = total;
  }
  skip_num += 1;
}

