import requests
import json
import time
import schedule
import threading
from typing import List, Dict, Any
import telebot


class SoumScraper:
    """A scraper for Soum.sa website using Typesense search API."""
    
    def __init__(self, api_key: str, base_url: str):
        """
        Initialize the scraper with API credentials.
        
        Args:
            api_key: Typesense API key
            base_url: Typesense API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = self._setup_headers()
    
    def _setup_headers(self) -> Dict[str, str]:
        """Setup HTTP headers for the API request."""
        return {
            'authority': self.base_url.split('//')[1].split('/')[0],
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ar-SA,ar;q=0.9,en-SA;q=0.8,en;q=0.7,en-US;q=0.6',
            'content-type': 'application/json',
            'origin': 'https://soum.sa',
            'referer': 'https://soum.sa/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-typesense-api-key': self.api_key,
        }
    
    def _create_search_payload(self, page: int) -> Dict[str, Any]:
        """Create the search payload for the API request."""
        # المتجه الثابت من الكود الأصلي
        vector_values = [
            0.059868544, -0.026311623, -0.05212315, -0.040056325, 0.012913228, 0.04020147,
            -0.010643969, 0.043931603, 0.021384345, 0.023778606, 0.041743517, 0.030075269,
            -0.017834593, -0.006639504, 0.013574437, -0.029372018, 0.020123802, -0.00826768,
            0.023135172, -0.04215364, -0.020143745, 0.018858982, 0.010974512, 0.05421099,
            0.001932559, -0.024146933, 0.032559056, -0.028032131, -0.03195458, 0.0027850962,
            -0.036883958, 0.039814018, -0.08346261, -0.017926052, 0.0280785, -0.058871545,
            -0.032643583, -0.0050886353, 0.00969865, 0.0005007084, 0.019731699, -0.059776068,
            0.00090990786, 0.02210365, 0.010548367, -0.027658038, 0.037709877, -0.0063742218,
            0.017867142, -0.0431956, 0.050899614, -0.026043594, 0.044576496, -0.021899218,
            0.016702127, -0.04915611, -0.008637916, 0.033647884, -0.0065736575, 0.009527646,
            -0.031046463, 0.019167606, -0.061265327, 0.04165765, 0.005938428, -0.030917596,
            -0.030254163, 0.015935749, 0.027694711, -0.032381345, -0.060924526, -0.0036338961,
            0.020623231, -0.014222013, -0.02184914, -0.06861312, -0.007217985, 0.025152931,
            0.013835272, 0.0196209, -0.031725205, -0.0069929985, -0.07475996, -0.01722602,
            -0.045375068, 0.0157236, -0.0007755267, 0.018478595, -0.0024527581, 0.070764184,
            -0.01242476, -0.013660156, 0.04413066, -0.08794731, 0.020571591, 0.03560328,
            0.0114517575, -0.027767438, 0.0017944751, -0.0039604637, -0.004543227, -0.024186593,
            0.01209238, 0.018678358, 0.025198149, -0.0016754795, -0.017986054, 0.007940052,
            -0.010313163, -0.02722727, -0.06137393, 0.020750284, 0.024115669, 0.016786741,
            0.034359753, -0.009068337, -0.03107612, 0.09726591, 0.008823852, 0.021703174,
            -0.017664772, -0.029876098, 0.082823485, 0.020020895, -0.01043637, -0.014426481,
            0.02968827, 0.04153898, 0.036724385, 0.0141079435, -0.046631485, -0.046546478,
            -0.011108943, -0.03350806, 0.09380104, 0.061912958, 0.038115345, 0.04771432,
            0.031100098, -0.027535858, 0.014189359, -0.018842641, -0.011475378, 0.016232992,
            -0.036990773, 0.04967701, -0.0070168944, -0.08134906, 0.015779935, -0.02223735,
            0.009354512, -0.008159892, -0.027083313, -0.011399344, 0.020851495, -0.015461607,
            -0.026970739, 0.014756361, 0.018202437, 0.023152903, 0.004092388, 0.011083422,
            0.03013689, 0.024560932, -0.040296312, -0.028621703, 0.012295327, -0.018533899,
            0.0053195455, 0.04011216, -0.02076534, 0.049724985, -0.06504871, -0.035373032,
            -0.055003624, -0.04561455, 0.001562131, -0.015393547, -0.012446039, 0.0015358011,
            -0.05016279, -0.041028682, 0.057271034, 0.03810912, 0.016133774, -0.019735008,
            0.03340901, -0.051051833, -0.017172396, -0.007113238, -0.00052389776, -0.0030304887,
            -0.040085793, 0.017086301, -0.019171571, 0.0017761928, 0.0013992668, 0.037046995,
            0.01227941, -0.030616365, 0.021829532, 0.04013184, -0.031639148, 0.027405895,
            0.030502047, -0.019388244, 0.077216305, -0.064402394, 0.023215663, 0.022650711,
            -0.040519513, 0.045714322, -0.0243721, 0.05280423, 0.034286782, -0.0030271586,
            0.038874403, 0.04141912, 0.01543107, 0.0024103946, -0.018575504, -0.042769667,
            0.0010386747, -0.017634373, 0.0037054804, 0.025971415, -0.024329595, -0.0036574723,
            0.025456384, -0.006783323, 0.012577107, 0.06501718, 0.044537533, 0.00955474,
            0.07132041, -0.042669322, -0.020240972, 0.002381538, -0.004704534, 0.024507716,
            -0.05118058, 0.028306806, 0.030003509, -0.022590267, -0.06264177, -0.03621162,
            -0.025426768, 0.022988033, -0.04016756, -0.018015293, -0.011170644, -0.014551719,
            0.031185811, 0.025696306, -0.065862, 0.011486043, -0.10737769, 0.023930207,
            0.0066198194, -0.021453645, 0.06287704, 0.04061692, -0.013161089, -0.006488798,
            -0.046260763, 0.027635586, -0.029072993, -0.039116547, -0.027743595, 0.006868883,
            0.02502902, -0.02188032, 0.050474156, 0.022333866, -0.018072527, 0.030224415,
            -0.01278603, 0.016390542, 0.0034254047, 0.0005835922, 0.017208705, 0.050388683,
            0.00955744, -0.030827269, -0.039515402, 0.025141653, -0.030433591, -0.012124927,
            0.03262805, 0.002236377, -0.099054836, -0.024716765, -0.007403591, -0.022413272,
            -0.03297924, 0.03427414, -0.015834622, 0.047130566, 0.07393744, 0.008889091,
            0.027839938, -0.05492015, 0.013704803, -0.08687673, 0.016003434, -0.013656256,
            -0.050449442, -0.05088718, 0.018653704, -0.0073670554, 0.02476639, -0.0052831136,
            -0.04826684, 0.027394388, 0.08583365, -0.0031714377, -0.038393147, 0.039109174,
            -0.019728843, 0.047955543, -0.015213976, 0.04820646, 0.016606791, -0.022737248,
            -0.004196703, -0.027064221, -0.010538642, 0.040022057, -0.001260021, -0.02134958,
            -0.031029975, 0.05753032, -0.029206323, 0.033661548, 0.0125873145, 0.021230016,
            -0.07729167, -0.033987787, -0.060876943, -0.012410165, 0.027239751, 0.022974044,
            -0.026224352, -0.09147176, 0.03701332, -0.0016826099, -0.006920317, 0.016100006,
            0.039967474, 0.0016229948, -0.005759942, 0.039202467, -0.031493265, 0.0035685091,
            0.023878023, 0.020824479, 0.032764483, 0.03746369, 0.02818987, -0.024332874,
            -0.052563436, 0.02522142, 0.0039933743, -0.044127304, 0.029645897, 0.044922736,
            0.041542392, -0.04641147, -0.009505905, 0.0124728205, 0.0070266393, -0.0429051,
            0.026197392, -0.010618201, -0.04805873, -0.057985667, -0.063198425, -0.015667915,
            0.06568963, -0.0032365022, -0.003689407, -0.021138495, 0.06293564, -0.007367908,
            -0.009258905, -0.020600071, 0.09804895, 0.05132791, 0.03728806, -0.03336886,
            0.0380084, 0.023556605, 0.050772864, -0.022565013, 0.01371631, -0.07767183,
            -0.034360968, -0.010199205, 0.007588429, -0.012064458, -0.0038043514, 0.005010042,
            -0.024200456, -0.01152278, -0.049679577, -0.031162221, -0.0139711285, -0.0067931134,
            -0.059191108, -0.016205272, 0.06798925, 0.034095496, 0.04773742, -0.0650419,
            -0.021954773, 0.008790556, 0.063623056, -0.04152278, 0.023173038, 0.016467597,
            -0.023545014, 0.041332114, 0.00012493119, -0.014712169, 0.003986058, -0.036869086,
            -0.0013793418, -0.007799543, 0.005651896, 0.10482212, 0.038680036, 0.041622877,
            0.0077160606, -0.0029257834, -0.013266425, -0.045120027, -0.0014527662, 0.051417787,
            -0.029104467, 0.0031522808, -0.017223775, -0.00033797018, 0.029590603, -0.059547666,
            -0.09387948, -0.07333545, 0.017531952, 0.012273459, 0.07336573, -0.107913636,
            -0.014682264, -0.04824141, -0.010939521, -0.09410252, -0.021321902, -0.022425674,
            0.048990663, 0.01814163, -0.033509217, -0.016557168, -0.057602484, -0.006304672,
            0.01701837, -0.09240486, 0.057972316, -0.0009950419, 0.032321528, -0.015024951,
            -0.037840687, 0.05056298, 0.018574178, -0.051144946, 0.012916473, -0.01077697,
            -0.01034851, 0.02510478, -0.05453696, -0.00863558, 0.026112849, -0.02774449,
            0.0075185793, -0.010798728, 0.03023963, 0.01560401, 0.0020612339, 0.0049061747,
            -0.026802232, -0.01830921, -0.015389513, 0.024144951, 0.008875034, -0.00050411624,
            0.011197548, -0.03678823, 0.005110146, -0.011968507, -0.016016161, -0.032245696,
            0.04703585, 0.0533597, -0.0064461874, -0.020634301, 0.012800484, -0.06587459,
            0.06588393, -0.10055337, -0.0015992293, -0.0036360226, -0.052691784, -0.030611798,
            -0.048059814, 0.022325853, 0.012426127, -0.055384576, 0.047386978, 0.023956029,
            -0.033178695, -0.019811993, 0.014494991, -0.020694243, 0.09393518, -0.008502595,
            -0.12072558, -0.0020096549, 0.0035866408, -0.0053074444, -0.04749729, 0.05298673,
            -0.010081004, -0.010436324, -0.04997088, 0.07624043, -0.0730033, -0.015079435,
            -0.040535774, 0.017307343, -0.008116331, 0.017514884, 0.057359762, 0.042578254,
            -0.01910587, -0.029283157, 0.012321081, 0.01653241, 0.040952228, 0.022891864,
            0.029985702, -0.067275494, 0.015715675, -0.013427666, -0.033307396, -0.029588804,
            0.015900131, 0.019472817, 0.02403828, 0.019990802, -0.040967975, -0.024611963,
            0.00817571, 0.023374725, -0.007552011, -0.036916338, 0.011013436, 0.03800095,
            0.07520412, 0.011179072, 0.023011016, -0.015201788, 0.055661455, -0.022268092,
            0.013974421, 0.033549417, 0.05183501, -0.008477186, 0.01543452, -0.027649453,
            -0.02083788, -0.014959227, -0.033536132, 0.016441366, 0.054242514, 0.020720642,
            0.009945168, 0.018269517, -0.04660466, -0.0051022694, -0.0036592637, -0.017233169,
            -0.004650412, -0.011894177, -0.046573568, 0.025176544, -0.03138517, 0.009959424,
            -0.009686828, -0.019314883, 0.030671619, 0.0020786899, 0.04906343, -0.0071144705,
            -0.022789625, -0.037012827, 0.12166033, -0.045119986, 0.076195285, 0.0092603145,
            -0.019685049, -0.035145387, -0.0006435259, 0.035888314, -0.0056132744, -0.0021271268,
            0.00825221, 0.021191377, -0.029598847, -0.0033997134, 0.064929895, 0.00087355287,
            -0.041994296, -0.03528865, -0.023687754, -0.018823745, 0.015613528, 0.048272192,
            0.011564728, -0.0027090071, -0.003972273, -0.020837825, 0.049350757, 0.08166901,
            0.033067685, 0.06930103, -0.016836448, 0.0065828813, -0.033762798, 0.0038083305,
            0.0329513, 0.0195134, -0.024615057, 0.05351378, -0.108783774, -0.032366917,
            0.06993263, -0.005164848, 0.0091293445, 0.05510734, 0.021672042, -0.027639804,
            -0.075294614, -0.018844463, -0.049601067, -0.044180494, -0.016232885, -0.023243075,
            0.003449206, 0.011003031, -0.0023528289, -0.016100835, 0.0036020104, -0.04061405,
            -0.027286194, 0.0422149, -0.027947377, -0.018837484, 0.001315214, 0.0024113297,
            -0.044075463, -0.066321135, -0.01773768, 0.012569984, -0.06812215, 0.065735474,
            0.016256696, -0.0024779702, 0.030637909, 0.008456276, 0.037222784, 0.047021635,
            0.023288632, 0.044332046, -0.020352254, -0.057413496, -0.018150538, -0.021907715,
            -0.019635456, 0.035325795, 0.035303973, 0.0012677887, -0.007072665, 0.0064298697,
            0.054844063, -0.067727566, -0.009893199, -0.009856092, 0.047547743, 0.0011295624,
            -0.015989564, -0.0041399896, -0.00921122, 0.036894795, -0.019758055, 0.02129529,
            0.0051439046, 0.018678028, 0.0004255291, 0.004835121, -0.011798454, 0.009453051,
            0.024253096, 0.055832144, 0.038489755, -0.038054965, -0.06400835, -0.019586269,
            -0.008271416, 0.005820991, 0.01717207, -0.029328058, -0.03807545, 0.073375575,
            -0.07179795, -0.017628545, 0.028171087, -0.08132413, 0.0043605436, 0.025292858,
            -0.026807413, 0.07986172, -0.0017790318, -0.06370561, 0.04711196, -0.0652024,
            -0.044845264, -0.023871703, -0.06028256, 0.0415859, -0.04622225, 0.053629026,
            -0.027648263, -0.01332238, -0.029164849, -0.00865177, 0.016652687, 0.023792878,
            0.0074285464, 0.009046685, 0.04924831, 0.0031503884, 0.029087428, -0.030611804,
            -0.070806414, -0.014481973, 0.006199992, 0.03331324, 0.038850263, -0.009558167,
            -0.04131365, 0.026866993, 0.024342394, -0.006745814, -0.022817327, 0.013611819,
            0.008739189, 0.0057513095, -0.00036123648, 0.050220616, -0.025459355, 0.012533285
        ]
        
        # بناء vector query بشكل صحيح
        vector_query = f"searchVector:({vector_values}, distance_threshold:0.35, k:10000)"
        
        return {
            "searches": [{
                "preset": "default-search",
                "per_page": 21,
                "exclude_fields": "searchVector,_vector_distance",
                "sort_by": "_vector_distance:asc",
                "collection": "products_production-sa",
                "q": "*",
                "filter_by": "sellPrice:<=1000000",
                "page": page,
                "vector_query": vector_query
            }]
        }
    def _extract_product_data(self, hit: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant product data from a search hit.
        
        Args:
            hit: A single search result hit
            
        Returns:
            Dictionary containing product information
        """
        document = hit.get("document", {})
        
        return {
            "name": document.get("arModelName", ""),
            "size": document.get("arVariantName", ""),
            "price": document.get("grandTotal", ""),
            "img": document.get("productImage", ""),
            "id": document.get("id", "")  # إضافة ID لتجنب التكرار
        }
    
    def scrape_products(self, pages: List[int]) -> List[Dict[str, Any]]:
        """
        Scrape products from multiple pages.
        
        Args:
            pages: List of page numbers to scrape
            
        Returns:
            List of product dictionaries
        """
        all_products = []
        
        for page in pages:
            try:
                payload = self._create_search_payload(page)
                
                response = requests.post(
                    f"{self.base_url}/multi_search",
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                
                data = response.json()
                hits = data["results"][0]["hits"]
                page_products = [self._extract_product_data(hit) for hit in hits]
                all_products.extend(page_products)
                
                print(f"Page {page}: Scraped {len(page_products)} products")
                
            except requests.exceptions.RequestException as e:
                print(f"Error scraping page {page}: {e}")
                continue
            except (KeyError, IndexError) as e:
                print(f"Error parsing response from page {page}: {e}")
                continue
        
        return all_products


class TelegramBot:
    """Telegram bot for sending product notifications."""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize the Telegram bot.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Chat ID to send messages to
        """
        self.bot = telebot.TeleBot(bot_token)
        self.chat_id = chat_id
        self.sent_products = set()  # لتجنب إرسال المنتجات المكررة
        
    def format_product_message(self, product: Dict[str, Any]) -> str:
        """Format product data into a readable message."""
        message = f"🛍️ **منتج جديد** 🛍️\n\n"
        message += f"**الاسم:** {product.get('name', 'غير متوفر')}\n"
        message += f"**المقاس:** {product.get('size', 'غير متوفر')}\n"
        message += f"**السعر:** {product.get('price', 'غير متوفر')} ريال\n"
        
        if product.get('img'):
            message += f"**الصورة:** {product['img']}\n"
        
        return message
    
    def send_product(self, product: Dict[str, Any]) -> bool:
        """
        Send a single product to Telegram.
        
        Args:
            product: Product data dictionary
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            product_id = product.get('id', '')
            if product_id in self.sent_products:
                print(f"Product {product_id} already sent, skipping...")
                return True
            
            message = self.format_product_message(product)
            
            # إذا كان هناك صورة، نرسل الصورة مع التسمية التوضيحية
            if product.get('img'):
                self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=product['img'],
                    caption=message,
                    parse_mode='Markdown'
                )
            else:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
            
            self.sent_products.add(product_id)
            print(f"✅ Product sent to Telegram: {product.get('name', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending product to Telegram: {e}")
            return False
    
    def send_products_batch(self, products: List[Dict[str, Any]]) -> None:
        """
        Send multiple products to Telegram with delays to avoid rate limiting.
        
        Args:
            products: List of product dictionaries
        """
        successful_sends = 0
        
        for i, product in enumerate(products):
            if self.send_product(product):
                successful_sends += 1
            
            # تأخير 2 ثانية بين كل رسالة لتجنب حظر التليجرام
            if i < len(products) - 1:
                time.sleep(2)
        
        print(f"📊 Sent {successful_sends}/{len(products)} products successfully")


class ProductMonitor:
    """Monitor products and send notifications to Telegram."""
    
    def __init__(self, scraper: SoumScraper, telegram_bot: TelegramBot):
        """
        Initialize the product monitor.
        
        Args:
            scraper: SoumScraper instance
            telegram_bot: TelegramBot instance
        """
        self.scraper = scraper
        self.bot = telegram_bot
        self.is_running = False
    
    def check_new_products(self) -> None:
        """Check for new products and send to Telegram."""
        print(f"🕒 Checking for new products at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # جلب المنتجات من الصفحات 1، 2، 3
            products = self.scraper.scrape_products([*range(1,56)])
            
            if products:
                print(f"📦 Found {len(products)} products")
                self.bot.send_products_batch(products)
                
                
                # إرسال ملخص
                summary_msg = f"✅ تم فحص المنتجات بنجاح\n🕒 الوقت: {time.strftime('%Y-%m-%d %H:%M:%S')}\n📊 العدد الإجمالي: {len(products)} منتج"
                self.bot.bot.send_message(self.bot.chat_id, summary_msg)
            else:
                print("❌ No products found")
                self.bot.bot.send_message(
                    self.bot.chat_id, 
                    f"⚠️ لم يتم العثور على منتجات\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
        except Exception as e:
            error_msg = f"❌ Error in product check: {e}"
            print(error_msg)
            self.bot.bot.send_message(self.bot.chat_id, error_msg)
    
    def start_monitoring(self, interval_minutes: int = 1) -> None:
        """
        Start monitoring products at regular intervals.
        
        Args:
            interval_minutes: Monitoring interval in minutes
        """
        self.is_running = True
        
        # الجولة الأولى فوراً
        #self.check_new_products()
        
        # جدولة الفحوصات الدورية
        schedule.every(interval_minutes).minutes.do(self.check_new_products)
        
        print(f"🚀 Started monitoring every {interval_minutes} minute(s)")
        self.bot.bot.send_message(
            self.bot.chat_id, 
            f"🚀 بدء المراقبة\n⏰ كل {interval_minutes} دقيقة\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # تشغيل الجدولة في thread منفصل
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop the monitoring process."""
        self.is_running = False
        print("⏹️ Monitoring stopped")
        self.bot.bot.send_message(
            self.bot.chat_id, 
            f"⏹️ توقفت المراقبة\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )


def main():
    """Main function to start the monitoring system."""
    # Configuration
    TYPESENSE_API_KEY = "9RPwj65iRtNHpqQqARO94Wx2lWEEOCWS"
    TYPESENSE_BASE_URL = "https://hy5cogiue4fnk2d0p.a1.typesense.net"
    
    # Telegram Configuration - استبدل هذه بالقيم الحقيقية
    TELEGRAM_BOT_TOKEN = "1909407635:AAEcNvsunfle52fZh_kcvaeANwiBtvOGXDk"  # احصل عليه من @BotFather
    TELEGRAM_CHAT_ID = "1414397128"  # احصل عليه من @userinfobot
    
    # Initialize components
    scraper = SoumScraper(api_key=TYPESENSE_API_KEY, base_url=TYPESENSE_BASE_URL)
    telegram_bot = TelegramBot(bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
    monitor = ProductMonitor(scraper=scraper, telegram_bot=telegram_bot)
    
    try:
        # Start monitoring every minute
        monitor.start_monitoring(interval_minutes=1)
        
        # Keep the script running
        print("Press Ctrl+C to stop monitoring...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping monitor...")
        monitor.stop_monitoring()
    except Exception as e:
        print(f"Unexpected error: {e}")
        monitor.stop_monitoring()


if __name__ == "__main__":
    main()
