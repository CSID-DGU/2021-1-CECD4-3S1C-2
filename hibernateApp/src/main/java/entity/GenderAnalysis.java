package entity;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Objects;

@Entity
public class GenderAnalysis implements Serializable {

    private int genderId;
    private double male;
    private double female;

    @Id
    @Column(name = "gender_id")
    public int getGenderId() {
        return genderId;
    }

    public void setGenderId(int genderId) {
        this.genderId = genderId;
    }

    @Basic
    @Column(name = "male")
    public double getMale() {
        return male;
    }

    public void setMale(double male) {
        this.male = male;
    }

    @Basic
    @Column(name = "female")
    public double getFemale() {
        return female;
    }

    public void setFemale(double female) {
        this.female = female;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        GenderAnalysis that = (GenderAnalysis) o;
        return genderId == that.genderId && Double.compare(that.male, male) == 0 && Double.compare(that.female, female) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(genderId, male, female);
    }
}
