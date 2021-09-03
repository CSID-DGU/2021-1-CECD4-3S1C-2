package main;

import entity.News;
import org.hibernate.type.StringType;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

import java.sql.Timestamp;
import java.lang.Long;

public class Main {
    public static void main(String[] args) {
        EntityManagerFactory entityManagerFactory = Persistence.createEntityManagerFactory("default");
        EntityManager entityManager = entityManagerFactory.createEntityManager();
        EntityTransaction transaction = entityManager.getTransaction();

        try{
            transaction.begin();

            News test_news = new News();
//            Comments test_comments = new Comments();
//            Genderanalysis test_gender = new Genderanalysis();
//            Ageanalysis test_age = new Ageanalysis();

            Timestamp time = Timestamp.valueOf("2021-09-03 03:15:00");

            test_news.setUrl("test url");
            test_news.setTitle("test title");
            test_news.setDate(time);
            test_news.setNewsId(11);

//            test_news.getTitle();

//            test_comments.setCommentsId(17000);
//            test_comments.setDate(time);
//            test_comments.setContents("test contents");
//            test_comments.set

            entityManager.persist(test_news);

            transaction.commit();
        } finally {
            if(transaction.isActive()){
                transaction.rollback();
            }
            entityManager.close();
            entityManagerFactory.close();
        }
    }
}
