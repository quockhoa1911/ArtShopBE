from api_product.models import Products, AuctionProduct
from api_base.services import Send_Mail_Service, Multi_Thread
from api_base.email_template import template


class AuctionProductService:

    @classmethod
    def create(cls, request, data):
        auction_price = data["auction_price"]
        product = Products.objects.filter(pk=data["product_id"]).first()
        if float(auction_price) < float(product.price):
            return {"message": "The price auction must larger than starting price"}, False
        if product and float(auction_price) > float(product.auction_price) and float(auction_price) > float(
                product.price):
            AuctionProduct(product=product, auction_price=auction_price, is_success=True, user=request.user).save()
            product.auction_price = auction_price
            product.save()
            return {"message": "Auction Success"}, True
        else:
            return {"message": "The price auction is not valid"}, False

    @classmethod
    def approve_auction(cls, pk):
        auction_product = AuctionProduct.objects.filter(pk=pk)
        if auction_product.exists():
            auction_product = auction_product.first()
            auction_product.is_success = True
            auction_product.save()
            auction_product.product.sold = True
            auction_product.product.save()

            string_html = template

            multi_thread = Multi_Thread(html=string_html, target=Send_Mail_Service.send_mail,
                                        content_main_body='Content_main_body', header='Auction success',
                                        from_email='noreply@gmail.com',
                                        to_emails=[auction_product.user.email])
            multi_thread.start()

            return {"message": "Approve Auction Success"}, True
        else:
            return {"message": "No Auction in data"}, False
