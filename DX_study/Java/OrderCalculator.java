public class OrderCalculator {

    public static void main(String[] args) {
        int total = calculateTotal(12000, 3);
        int total2 = calculateTotal(12000, 5);
        int total3 = calculateTotal(12000, 10);
        

        System.out.println("총 금액: " + total);
        System.out.println("총 금액: " + total2);
        System.out.println("총 금액: " + total3);
        
    }

		//메서드 선언 
    public static int calculateTotal(int price, int quantity) {
        return price * quantity;
    }
}