package main;

import entity.News;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface repositoryNews extends JpaRepository<News, Integer> {
    List<News> findByNewsId(int newsId);

}
