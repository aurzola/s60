package com.aurzola.s60.charserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class CharserverApplication {

	public static void main(String[] args) {
		SpringApplication.run(CharserverApplication.class, args);
	}

}
