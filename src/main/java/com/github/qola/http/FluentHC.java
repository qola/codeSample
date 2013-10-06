package com.github.qola.http;

import org.apache.http.client.fluent.Form;
import org.apache.http.client.fluent.Request;

import java.io.IOException;

/**
 * Created with IntelliJ IDEA.
 * User: leejonghee
 * Date: 13. 10. 6.
 * Time: 오후 3:06
 * To change this template use File | Settings | File Templates.
 */
public class FluentHC {

    public String get() throws IOException {
        String result =Request.Get("http://targethost/homepage")
                .execute().returnContent().toString();
        return result;
    }

    public String post() throws IOException {
        String result  = Request.Post("http://targethost/login")
                .bodyForm(Form.form().add("username",  "vip").add("password",  "secret").build())
                .execute().returnContent().toString();
        return result;

    }




}
