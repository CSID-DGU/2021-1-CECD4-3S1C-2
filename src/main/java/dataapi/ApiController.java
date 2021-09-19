package dataapi;

import org.springframework.web.bind.annotation.*;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;


@CrossOrigin("*")
@RestController
public class ApiController {
    @RequestMapping(value="/api/data", method = RequestMethod.GET)
//    @ResponseStatus(value = HttpStatus.OK)
    public JSONArray getData(){
        JSONArray dataArray = new JSONArray();
        JSONObject one = new JSONObject();
        JSONObject two = new JSONObject();
        JSONObject three = new JSONObject();
        JSONObject four = new JSONObject();
        JSONObject five = new JSONObject();
        JSONObject six = new JSONObject();
        JSONObject seven = new JSONObject();
        JSONObject eight = new JSONObject();

        one.put("keyword", "Frozen Yogurt");
        two.put("keyword", "Ice cream sandwich");
        three.put("keyword", "Eclair");
        four.put("keyword", "Cupcake");
        five.put("keyword", "Gingerbread");
        six.put("keyword", "Jelly bean");
        seven.put("keyword", "Lollipop");
        eight.put("keyword", "Honeycomb");


        dataArray.add(one);
        dataArray.add(two);
        dataArray.add(three);
        dataArray.add(four);
        dataArray.add(five);
        dataArray.add(six);
        dataArray.add(seven);
        dataArray.add(eight);

        return dataArray;
    }

    @RequestMapping(value="/api/StringData", method = RequestMethod.GET)
//    @ResponseStatus(value = HttpStatus.OK)
    public String getStringData(){

        String result = "Hi";

        return result;
    }
}
