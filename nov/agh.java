class Student { int roll;
String name; Student(int r, String n) { roll = r;
name = n;
}
void display(Student s) { System.out.println("Roll No: " + s.roll); System.out.println("Name: " + s.name);
}

Student changeData() {
Student temp = new Student(43, "Ujjaldeep"); return temp;
}
}

public class agh {
public static void main(String[] args) { Student s1 = new Student(42, "Riishabh");
System.out.println("Passing Object as Parameter:"); s1.display(s1);

System.out.println("\nReturning Object from Method:"); Student s2 = s1.changeData();
s2.display(s2);
}
}
