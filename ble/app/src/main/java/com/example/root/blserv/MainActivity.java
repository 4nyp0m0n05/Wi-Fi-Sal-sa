package com.example.root.blserv;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.IntentFilter;
import android.os.SystemClock;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;


import android.bluetooth.BluetoothSocket;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

import java.io.DataInputStream;
import java.util.Arrays;
import java.util.Set;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;
import java.util.UUID;

import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ArrayAdapter;
import android.content.Intent;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import android.widget.EditText;
public class MainActivity extends AppCompatActivity {


    private BluetoothAdapter BTAdapter = BluetoothAdapter.getDefaultAdapter();
    private Set<BluetoothDevice>pairedDevices;
    BluetoothSocket mmSocket;
    BluetoothDevice mmDevice;
    private String EXTRA_ADDRESS = null;
    private ListView lv;
    private int ten=0;

    
    private final BroadcastReceiver mReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);

            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                Toast.makeText(getApplicationContext(),action.toString(),Toast.LENGTH_SHORT).show();
            }
            else if (BluetoothDevice.ACTION_ACL_CONNECTED.equals(action)) {
                Toast.makeText(getApplicationContext(),action.toString(),Toast.LENGTH_SHORT).show();
            }
            else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
                Toast.makeText(getApplicationContext(),action.toString(),Toast.LENGTH_SHORT).show();
            }
            else if (BluetoothDevice.ACTION_ACL_DISCONNECT_REQUESTED.equals(action)) {
                Toast.makeText(getApplicationContext(),action.toString(),Toast.LENGTH_SHORT).show();
            }
            else if (BluetoothDevice.ACTION_ACL_DISCONNECTED.equals(action)) {
                Toast.makeText(getApplicationContext(),action.toString(),Toast.LENGTH_SHORT).show();
                ten=0;
            }
        }
    };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        Button btnSend=(Button)findViewById(R.id.button3);
        Button btnConnect=(Button)findViewById(R.id.button5);
        
        IntentFilter filter = new IntentFilter();
        filter.addAction(BluetoothDevice.ACTION_ACL_CONNECTED);
        filter.addAction(BluetoothDevice.ACTION_ACL_DISCONNECT_REQUESTED);
        filter.addAction(BluetoothDevice.ACTION_ACL_DISCONNECTED);
        this.registerReceiver(mReceiver, filter);


       
        btnConnect.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    
                    if (ten != 1) {
                        BluetoothSocket tmp = null;
                        final BluetoothDevice device = BTAdapter.getRemoteDevice(EXTRA_ADDRESS);
                        mmDevice = device;
                        try {
                            UUID uuid = UUID.fromString("");//uuid
                            tmp = mmDevice.createRfcommSocketToServiceRecord(uuid);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        mmSocket = tmp;
                        BTAdapter.cancelDiscovery();
                        try {
                            mmSocket.connect();
                        } catch (IOException connectException) {

                            try {
                                mmSocket.close();
                   
                            } catch (IOException closeException) {
                                closeException.printStackTrace();
                            }
                        }
                    }
                    ten = 1;
                } catch (Exception e) {
                    e.printStackTrace();
                }

            } });
        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                
                final BluetoothDevice device = BTAdapter.getRemoteDevice(EXTRA_ADDRESS);
                try {
                    
                    if (ten!=1) {
                        BluetoothSocket tmp = null;
                        mmDevice = device;
                        try {
                            UUID uuid = UUID.fromString("");//uuid
                            tmp = mmDevice.createRfcommSocketToServiceRecord(uuid);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        mmSocket = tmp;
                        BTAdapter.cancelDiscovery();
                        try {
                            mmSocket.connect();
                        } catch (IOException connectException) {

                            try {
                                mmSocket.close();
                    
                            } catch (IOException closeException) {
                                closeException.printStackTrace();
                            }
                        }
                    }
                    EditText editText=(EditText)findViewById(R.id.editText);
                    String msg =editText.getText().toString();
                    OutputStream mmOutputStream = mmSocket.getOutputStream();
                    mmOutputStream.write(msg.getBytes());
                    SystemClock.sleep(3000);
                    if(mmSocket.isConnected()&&!msg.contains("10")&&!msg.contains("13")){
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                int data1;
                                try{
                                    InputStream inputStream = mmSocket.getInputStream();
                                    DataInputStream dataInputStream=new DataInputStream(inputStream);
                                    data1=inputStream.available();
                                    byte[] packet = new byte[data1];
                                    dataInputStream.readFully(packet, 0, packet.length);
                                    if(packet.length>0)
                                        Toast.makeText(getApplicationContext(),new String(packet),Toast.LENGTH_SHORT).show();
                                }catch (Exception e){
                                    Log.e("error",e.toString());
                                }
                            }
                        });

                    }

                    if (msg.contains("10") || msg.contains("13")){
                        runOnUiThread(new Runnable() {
                                          @Override
                                          public void run() {
                                              int bytes_available;
                                              int bytes_count;
                                              String strget;
                                              try {
                                                  InputStream inputStream = mmSocket.getInputStream();
                                                  DataInputStream dataInputStream=new DataInputStream(inputStream);
                                                  bytes_available=inputStream.available();
                                                  byte[] packetBytes = new byte[bytes_available];
                                                  dataInputStream.readFully(packetBytes, 0, packetBytes.length);
                                                  Log.e("data",new String(packetBytes));
                                                 

                                                  if(packetBytes.length>0) {
                                                      Intent intent = new Intent(MainActivity.this, Main2Activity.class);
                                                      intent.putExtra("data", new String(packetBytes));
                                                      startActivity(intent);
                                                  }
                                                 
                                              } catch (IOException e) {
                                                  e.printStackTrace();
                                              }
                                          }
                                      });


                    }

                    ten=1;
                } catch (IOException e) {
                    e.printStackTrace();
                }


            }
        });

        Button btnOn=(Button)findViewById(R.id.button);
        Button btnOff=(Button)findViewById(R.id.button2);

        btnOn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!BTAdapter.isEnabled()){
                    Intent turnOn = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                    startActivityForResult(turnOn, 0);
                }

            }
        });
        btnOff.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(BTAdapter.isEnabled()){
                    BTAdapter.disable();
                }
                try{
                    ten=0;
                    if (mmSocket!=null)
                        mmSocket.close();

                }
                catch (IOException e){
                    e.printStackTrace();
                }
            }
        });

        Button btnP=(Button)findViewById(R.id.button4);
        btnP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                deviceList();
            }
        });


    }
    public void deviceList(){
        ArrayList deviceList = new ArrayList();
        pairedDevices = BTAdapter.getBondedDevices();

        if (pairedDevices.size() > 0) {
            for (BluetoothDevice bt : pairedDevices) deviceList.add(bt.getName() + " " + bt.getAddress());
            Toast.makeText(getApplicationContext(), "Showing paired devices", Toast.LENGTH_SHORT).show();
            final ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, deviceList);
            ListView lv = (ListView)findViewById(R.id.listView);
            lv.setAdapter(adapter);
            lv.setOnItemClickListener(myListClickListener);
        }
    }
    private AdapterView.OnItemClickListener myListClickListener = new AdapterView.OnItemClickListener() {

        @Override
        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
            String info = ((TextView) view).getText().toString();
            String address = info.substring(info.length() - 17);
            EXTRA_ADDRESS=address;

        }
    };
    @Override
    protected void onStop() {
        super.onStop();
        if(mmSocket!=null){
            try {
                mmSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
