import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

public class DiscountCalculator {

    // Python의 def calculate_discount_price(price): 에 해당
    public static int calculateDiscountPrice(int price) {
        if (price >= 200000) {
            return price * 90 / 100;
        } else if (price >= 50000) {
            return price * 95 / 100;
        } else {
            return price;
        }
    }

    public static void main(String[] args) {

        // 상품 가격 (Python의 product_prices 딕셔너리)
        LinkedHashMap<String, Integer> productPrices = new LinkedHashMap<>();
        productPrices.put("키보드", 50000);
        productPrices.put("마우스", 30000);
        productPrices.put("모니터", 250000);
        productPrices.put("웹캠", 80000);
        productPrices.put("스피커", 120000);

        // 상품 카테고리 (Python의 product_categories 딕셔너리)
        LinkedHashMap<String, String> productCategories = new LinkedHashMap<>();
        productCategories.put("키보드", "주변기기");
        productCategories.put("마우스", "주변기기");
        productCategories.put("모니터", "전자기기");
        productCategories.put("웹캠", "전자기기");
        productCategories.put("스피커", "음향기기");

        // 상품 재고 (Python의 product_stocks 딕셔너리)
        LinkedHashMap<String, Integer> productStocks = new LinkedHashMap<>();
        productStocks.put("키보드", 5);
        productStocks.put("마우스", 10);
        productStocks.put("모니터", 2);
        productStocks.put("웹캠", 0);
        productStocks.put("스피커", 3);

        // 대상 카테고리 (Python의 target_categories 집합)
        Set<String> targetCategories = new HashSet<>();
        targetCategories.add("주변기기");
        targetCategories.add("전자기기");

        // 결과를 담을 변수들
        ArrayList<String> selectedProducts = new ArrayList<>();
        int total = 0;
        int soldOutCount = 0;

        // Python의 for name, price in product_prices.items():
        for (Map.Entry<String, Integer> entry : productPrices.entrySet()) {
            String name = entry.getKey();
            int price = entry.getValue();

            String category = productCategories.get(name);
            int stock = productStocks.get(name);

            if (stock == 0) {
                soldOutCount = soldOutCount + 1;
            } else {
                if (targetCategories.contains(category) && price >= 50000) {
                    int discountPrice = calculateDiscountPrice(price);
                    selectedProducts.add(name);
                    total = total + discountPrice;
                }
            }
        }

        // Python이 리스트를 ['키보드', '모니터'] 형태로 출력하므로 동일하게 맞춰줌
        String listText = "[";
        for (int i = 0; i < selectedProducts.size(); i++) {
            if (i > 0) {
                listText = listText + ", ";
            }
            listText = listText + "'" + selectedProducts.get(i) + "'";
        }
        listText = listText + "]";

        System.out.println("구매 대상 상품: " + listText);
        System.out.println("할인 적용 합계: " + total + "원");
        System.out.println("품절 상품 개수: " + soldOutCount + "개");
    }
}