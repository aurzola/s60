package com.aurzola.s60.charserver;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import java.util.*;
import java.util.stream.Collectors;

import org.springframework.core.io.ClassPathResource;
import org.springframework.http.MediaType;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import javax.servlet.http.HttpServletResponse;

@RestController
public class MyRestController {
    private static final int DISPLAYSIZE = 12;
    private static String message="0123456789ABCDFG";
    private static  Map<String, Integer> imeiToPos; 
    private static List<String> messages = new ArrayList<>();
    private static int index =0;
    @PostConstruct
    private void initImei2pos() throws IOException {
        imeiToPos = new HashMap<>();
        Properties props = readPropertiesFile("imeitopos.properties");
        if ( props != null)
            for( Map.Entry<Object, Object> e: props.entrySet()) {
                imeiToPos.put(e.getKey().toString(), Integer.parseInt(e.getValue().toString()));
            }
    }

    @Scheduled(fixedDelay = 20000)
    public void scheduleFixedDelayTask() {
        if ( !messages.isEmpty()) {
            this.message = messages.get(index);
            index = ( index + 1 ) % messages.size();
            //System.out.println("rotating message - current:  " + this.message);
        }
    }


    @GetMapping("/add/{message}")
    public String addMessage(@PathVariable(required = true) String  message){
        String[] strings = splitIntoLine(message, DISPLAYSIZE);
        System.out.println("Adding new Message to the queue");
        for (String s: strings)
            messages.add(StringUtils.center(s, DISPLAYSIZE));
        return "OK";
    }


    @GetMapping("/set/{message}")
    public String setMessage(@PathVariable(required = true) String  message){
        System.out.println("Updating Message");
        this.message=message;
        return "OK";
    }

    @GetMapping("/del/{index}")
    public String delMessage(@PathVariable(required = true) int index){
        if ( index < messages.size() ) {
            System.out.println("Deleting Message from the queue");
            messages.remove(index);
            return "OK";
        } else
            return "Index out of bounds";

    }

    @GetMapping("/")
    public String getLetter(@RequestParam(required = true) int pos){
        System.out.println("===============================");
        System.out.println("Gettin letter for pos " + pos);
        if (pos < message.length())
            return message.substring(pos,pos+1);
        else         return "";
    }

    @GetMapping("/i")
    public String getCelLetter(@RequestParam(required = true) String imei){
        System.out.println("===============================");
        System.out.println("Gettin letter for imei " + imei);
        if ( imeiToPos.containsKey(imei) )
            if ( imeiToPos.get(imei) < message.length() )
                return message.substring(imeiToPos.get(imei),
                    imeiToPos.get(imei)+1);
            else
                return "";
        else  return "";
    }

   @GetMapping("/si")
   public String setCelLetter(@RequestParam(required = true) String imei, @RequestParam(required = true) Integer pos){
        if ( pos >= message.length() )
            return "NOK - Pos Beyond Message";
        System.out.println("===============================");

        imeiToPos.put(imei, pos);
        System.out.println(imeiToPos);
       try {
           saveProps();
           System.out.println("set pos for imei " + imei + " " + pos);
       } catch (IOException e) {
           e.printStackTrace();
       }
       return "Ok";
    }

    @GetMapping(
            value = "/img/{img}",
            produces = MediaType.IMAGE_JPEG_VALUE
    )
    public void getImageWithMediaType(HttpServletResponse response, @PathVariable(required = true) Integer img) throws IOException {
        ClassPathResource imgFile = new ClassPathResource("/static/" + img +".jpg");
        response.setContentType(MediaType.IMAGE_JPEG_VALUE);
        StreamUtils.copy(imgFile.getInputStream(), response.getOutputStream());
    }

    private  void saveProps() throws IOException {
        Properties props = new Properties();
        for(Map.Entry<String, Integer> e: imeiToPos.entrySet())
            props.put(e.getKey(), e.getValue().toString());

        String path = "imeitopos.properties";
        FileOutputStream outputStrem = new FileOutputStream(path);
        //Storing the properties file
        props.store(outputStrem, "properties file for mapping phone imei to char pos");
    }

    public  Properties readPropertiesFile(String fileName) throws IOException {
        FileInputStream fis = null;
        Properties prop = null;
        try {
            fis = new FileInputStream(fileName);
            prop = new Properties();
            prop.load(fis);
        } catch(FileNotFoundException fnfe) {
            fnfe.printStackTrace();
        } catch(IOException ioe) {
            ioe.printStackTrace();
        } finally {
            if (fis != null)
                fis.close();
        }
        return prop;
    }

    public String[] splitIntoLine(String input, int maxCharInLine){

        StringTokenizer tok = new StringTokenizer(input, " ");
        StringBuilder output = new StringBuilder(input.length());
        int lineLen = 0;
        while (tok.hasMoreTokens()) {
            String word = tok.nextToken();

            while(word.length() > maxCharInLine){
                output.append(word.substring(0, maxCharInLine-lineLen) + "\n");
                word = word.substring(maxCharInLine-lineLen);
                lineLen = 0;
            }

            if (lineLen + word.length() > maxCharInLine) {
                output.append("\n");
                lineLen = 0;
            }
            output.append(word + " ");

            lineLen += word.length() + 1;
        }

        return output.toString().split("\n");
    }


}