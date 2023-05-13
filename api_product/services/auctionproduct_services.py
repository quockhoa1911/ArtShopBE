from api_product.models import Products, AuctionProduct


class AuctionProductService:

    @classmethod
    def create(cls, request, data):
        auction_price = data["auction_price"]
        product = Products.objects.filter(pk=data["product"]).first()
        if float(auction_price) > float(product.auction_price if product.auction_price is not None else 0):
            AuctionProduct(product=product, auction_price=auction_price, is_success=True, user=request.user).save()
            product.auction_price = auction_price
            product.save()
            return {"message": "Auction Success"}, True
        else:
            return {"message": "The price auction is not valid"}, False
