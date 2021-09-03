package entity;

import javax.persistence.*;
import java.io.Serializable;
import java.sql.Timestamp;
import java.util.Objects;

@Entity
public class News implements Serializable{

    private int newsId;
    private String title;
    private String url;
    private Timestamp date;

    @Id
    @Column(name = "news_id")
    public int getNewsId() {
        return newsId;
    }

    public void setNewsId(int newsId) {
        this.newsId = newsId;
    }

    @Basic
    @Column(name = "title")
    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    @Basic
    @Column(name = "url")
    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    @Basic
    @Column(name = "date")
    public Timestamp getDate() {
        return date;
    }

    public void setDate(Timestamp date) {
        this.date = date;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        News news = (News) o;
        return newsId == news.newsId && Objects.equals(title, news.title) && Objects.equals(url, news.url) && Objects.equals(date, news.date);
    }

    @Override
    public int hashCode() {
        return Objects.hash(newsId, title, url, date);
    }
}
