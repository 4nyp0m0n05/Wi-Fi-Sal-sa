package edu.sakarya.testinet;

import android.content.Context;
import android.net.wifi.WifiManager;

class WifiController {

    Context activity;
    private WifiManager wifiManager;



    public WifiController(Context activity){
        this.activity = activity;
        wifiManager = (WifiManager) activity.getApplicationContext().getSystemService(Context.WIFI_SERVICE);

    }

    public boolean IsWifiEnabled(){
        return wifiManager.isWifiEnabled();
    }

    public void WifiEnabled(boolean bln){
        wifiManager.setWifiEnabled(bln);
    }
    public boolean ChangeWifiState(boolean bool){
        wifiManager.setWifiEnabled(!bool);
        
        return (!bool);

    }
}
