package entity;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Objects;

@Entity
public class AgeAnalysis implements Serializable{


    private int ageId;

    @Id
    @javax.persistence.Column(name = "age_id")
    public int getAgeId() {
        return ageId;
    }

    public void setAgeId(int ageId) {
        this.ageId = ageId;
    }

    private double tens;

    @Basic
    @javax.persistence.Column(name = "tens")
    public double getTens() {
        return tens;
    }

    public void setTens(double tens) {
        this.tens = tens;
    }

    private double twenties;

    @Basic
    @javax.persistence.Column(name = "twenties")
    public double getTwenties() {
        return twenties;
    }

    public void setTwenties(double twenties) {
        this.twenties = twenties;
    }

    private double thirties;

    @Basic
    @javax.persistence.Column(name = "thirties")
    public double getThirties() {
        return thirties;
    }

    public void setThirties(double thirties) {
        this.thirties = thirties;
    }

    private double fourties;

    @Basic
    @javax.persistence.Column(name = "fourties")
    public double getFourties() {
        return fourties;
    }

    public void setFourties(double fourties) {
        this.fourties = fourties;
    }

    private double fifties;

    @Basic
    @javax.persistence.Column(name = "fifties")
    public double getFifties() {
        return fifties;
    }

    public void setFifties(double fifties) {
        this.fifties = fifties;
    }

    private double sixties;

    @Basic
    @javax.persistence.Column(name = "sixties")
    public double getSixties() {
        return sixties;
    }

    public void setSixties(double sixties) {
        this.sixties = sixties;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AgeAnalysis that = (AgeAnalysis) o;
        return ageId == that.ageId && Double.compare(that.tens, tens) == 0 && Double.compare(that.twenties, twenties) == 0 && Double.compare(that.thirties, thirties) == 0 && Double.compare(that.fourties, fourties) == 0 && Double.compare(that.fifties, fifties) == 0 && Double.compare(that.sixties, sixties) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(ageId, tens, twenties, thirties, fourties, fifties, sixties);
    }
}
