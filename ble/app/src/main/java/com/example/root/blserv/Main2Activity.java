package com.example.root.blserv;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;

public class Main2Activity extends AppCompatActivity {
    private EditText editText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        editText=findViewById(R.id.editText4);
        editText.setFocusable(false);
        editText.setClickable(true);
        String s = getIntent().getStringExtra("data");
        //Log.e("data",s);
        editText.setText(s);

    }

}
