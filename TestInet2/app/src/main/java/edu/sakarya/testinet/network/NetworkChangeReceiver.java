package edu.sakarya.testinet.network;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;

import java.lang.ref.WeakReference;

public class NetworkChangeReceiver extends BroadcastReceiver {

    private WeakReference<NetworkChangeListener> mNetworkChangleListenerWR;


    @Override
    public void onReceive(Context context, Intent intent) {
        NetworkChangeListener networkChangeListener = mNetworkChangleListenerWR.get();
        if (networkChangeListener != null) {
            networkChangeListener.onNetworkChange(isNetworkConnected(context));
        }
    }

    void setNetworkChangeListener(NetworkChangeListener networkChangeListener) {
        mNetworkChangleListenerWR = new WeakReference<>(networkChangeListener);
    }

    void removeNetworkChangeListener() {
        if (mNetworkChangleListenerWR != null) {
            mNetworkChangleListenerWR.clear();
        }
    }

    boolean isNetworkConnected(Context context) {
        ConnectivityManager connectivityManager = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo netInfo = connectivityManager.getActiveNetworkInfo();

        //should check null because in airplane mode it will be null
        return netInfo != null && netInfo.isConnected();

    }

    interface NetworkChangeListener{
        void onNetworkChange(boolean isNetworkAvailable);
    }
}
