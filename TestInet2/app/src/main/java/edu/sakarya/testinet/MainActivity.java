package edu.sakarya.testinet;

import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import edu.sakarya.testinet.network.InternetAvailabilityChecker;
import edu.sakarya.testinet.network.InternetConnectivityListener;
import edu.sakarya.testinet.service.ForegroundNotificationService;
import edu.sakarya.testinet.wificontroller.WifiReceiver;


public class MainActivity extends AppCompatActivity implements InternetConnectivityListener {

    //Some Objects
    SslScanRunnable runnable;
    Handler handler;
    WifiManager wifiManager;
    WifiReceiver wifiReceiver;
    //Components
    private Button scanSslBttn, serviceBttn;
    private TextView textView, scanPercentText, connectStatText, wifiSSID, wifiFrequency, wifiMACText, wifiIPText, wifidBmText, wifiSpeedText;
    private ImageView imageView;
    private Switch wifiSwitch;
    //Values
    private Boolean isConnect = false;
    private InternetAvailabilityChecker mInternetAvailabilityChecker;

    @Override
    protected void onStart() {
        super.onStart();
        IntentFilter intentFilter = new IntentFilter(WifiManager.WIFI_STATE_CHANGED_ACTION);
        registerReceiver(wifiReceiver, intentFilter);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        textView = findViewById(R.id.textView);
        scanPercentText = findViewById(R.id.scanPercentText);
        scanSslBttn = findViewById(R.id.scanSslBttn);
        imageView = findViewById(R.id.ssl_status_image);
        connectStatText = findViewById(R.id.connectStatText);
        serviceBttn = findViewById(R.id.serviceBtn);
        wifiSwitch = findViewById(R.id.wifi_switch);
        wifiSSID = findViewById(R.id.wifi_ssid_text);
        wifiFrequency = findViewById(R.id.wifi_frequency_text);
        wifiMACText = findViewById(R.id.wifi_mac_text);
        wifiIPText = findViewById(R.id.wifi_ip_text);
        wifidBmText = findViewById(R.id.wifi_dBm_text);
        wifiSpeedText = findViewById(R.id.wifi_speed_text);

        //Special Object
        wifiManager = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        handler = new Handler();

        wifiReceiver = new WifiReceiver(wifiSwitch);

        runnable = new SslScanRunnable(this, handler, scanPercentText, imageView, textView);
        mInternetAvailabilityChecker = InternetAvailabilityChecker.getInstance();
        mInternetAvailabilityChecker.addInternetConnectivityListener(this);

        changeStatServiceBttn();

        scanSslBttn.setOnClickListener(this::ScanSsl);

        wifiSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> {
            if (isChecked) {
                //wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
                wifiManager.setWifiEnabled(true);
            } else {
                //wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
                wifiManager.setWifiEnabled(false);
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        changeStatServiceBttn();
    }

    public void ScanSsl(View v) {
        new Thread(runnable).start();
    }

    @Override
    protected void onStop() {
        super.onStop();
        unregisterReceiver(wifiReceiver);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mInternetAvailabilityChecker.removeInternetConnectivityChangeListener(this);
    }

    @Override
    public void onInternetConnectivityChanged(boolean isConnected) {
        if (isConnected) {
            connectStatText.setText("Connected");
            makeEnableButton(scanSslBttn);
            isConnect = true;
            if (wifiManager.isWifiEnabled()) {
                WifiInfo info = wifiManager.getConnectionInfo();
                wifiSSID.setText(info.getSSID());
                wifiFrequency.setText(String.valueOf(info.getFrequency()));
                wifiIPText.setText(String.valueOf(info.getIpAddress()));
                wifiSpeedText.setText(info.getLinkSpeed() + " Mbps");
                wifidBmText.setText(String.valueOf(info.getRssi()));
                wifiMACText.setText(String.valueOf(info.getMacAddress()));
            } else {

                wifiSSID.setText("Unknown");
                wifiFrequency.setText("Unknown");
                wifiIPText.setText("Unknown");
                wifiSpeedText.setText("Unknown");
                wifidBmText.setText("Unknown");
                wifiMACText.setText("Unknown");
            }
        } else {
            connectStatText.setText("Not Connect");
            makeDisableButton(scanSslBttn);
            imageView.setImageResource(R.drawable.ssl_unk);
            scanPercentText.setText("%_.__");
            textView.setText("Unknown");
            isConnect = false;

            wifiSSID.setText("...");
            wifiFrequency.setText("...");
            wifiIPText.setText("...");
            wifiSpeedText.setText("...");
            wifidBmText.setText("...");
            wifiMACText.setText("...");
        }
    }

    private void makeEnableButton(Button... bttns) {
        for (Button btn : bttns) {
            btn.setEnabled(true);
            btn.setBackgroundColor(Color.GREEN);
        }
    }

    private void makeDisableButton(Button... bttns) {
        for (Button btn : bttns) {
            btn.setEnabled(false);
            btn.setBackgroundColor(Color.GRAY);

        }
    }

    public void clickService(View v) {

        Intent serviceIntent = new Intent(this, ForegroundNotificationService.class);

        if (isServiceRunning()) {
            stopService(serviceIntent);
        } else {
            serviceIntent.putExtra("isConnect", isConnect);

            startService(serviceIntent);
        }
        changeStatServiceBttn();
    }


    public void isServiceExist(View v) {
        if (isServiceRunning()) {
            Toast.makeText(this, "service running", Toast.LENGTH_LONG).show();
        } else {
            Toast.makeText(this, "service not running", Toast.LENGTH_LONG).show();
        }
    }

    private boolean isServiceRunning() {
        ActivityManager manager = (ActivityManager) getSystemService(ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
            if ("edu.sakarya.testinet.service.ForegroundNotificationService".equals(service.service.getClassName())) {
                return true;
            }
        }
        return false;
    }

    private void changeStatServiceBttn() {
        if (isServiceRunning()) {
            serviceBttn.setBackgroundColor(Color.RED);
            serviceBttn.setText("STOP");
        } else {
            serviceBttn.setBackgroundColor(Color.GREEN);
            serviceBttn.setText("START");
        }
    }
}
