package com.adamsunderman.assistantmanager;

import android.support.v4.widget.SimpleCursorAdapter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.SimpleAdapter;
import android.widget.ListView;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONObject;
import org.json.*;
import android.*;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;


public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final String [] response_data = new String[1];
        OkHttpClient client = new OkHttpClient();
        okhttp3.Request emp_list_request = new okhttp3.Request.Builder().url("https://assistantmanagerags.appspot.com/employee").build();
        client.newCall(emp_list_request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }
            @Override
            public void onResponse(Call call, okhttp3.Response response) throws IOException {
                if(!response.isSuccessful()){
                    throw new IOException("Unexpected code "+ response);
                }
                response_data[0] = response.body().string();
            }
        });

        ListView listView =(ListView)findViewById(R.id.employee_list);
        ArrayList<HashMap<String, String>> arrayList=new ArrayList<>();
        try{
            JSONArray j2 = new JSONArray(response_data[0]);
            for(int i =0;i<j2.length();i++){
                JSONObject o = j2.getJSONObject(i);
                HashMap<String,String> hashMap=new HashMap<>();
                hashMap.put("name", o.getString("name"));
                hashMap.put("id", o.getString("link"));
                arrayList.add(hashMap);
            }
        }catch (JSONException e){
            e.printStackTrace();
        }
        String[] from = {"name","id"};
        int[] to ={R.id.employee_name_text,R.id.employee_id_text};
        SimpleAdapter simpleAdapter = new SimpleAdapter(MainActivity.this, arrayList, R.layout.list_template, from, to);
        listView.setAdapter(simpleAdapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Toast.makeText(getApplicationContext(),"Click",Toast.LENGTH_LONG).show();
            }
        });
    }
}
