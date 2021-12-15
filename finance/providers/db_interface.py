from users.providers import db_interface as users_db_interface
from finance.models import PaymentSystemTransaction, Transaction

'''
TODO to complete interface it is better to return custom object Transaction / Payment System Transaction
instead of Django ORM Models

Better would be, but TBD: 

class DB_Transaction:
    ModelClass = Transaction  # app / models 
    BusinessEntity = PowerPointsTransaction # app / domain / business entities
    
    def model_to_entity(model_obj): 
        # iter through model fields and map into BusinessEntity
        pass
        
    def entity_to_model(entity_obj):
        # iter through entity fields and map into ModelClass
        pass
    
class Selector(DB_Transaction):
    
     @staticmethod
     def get_transaction_by_id():
        transaction = self.ModelClass.objects.get(id=transaction_id)
        pp_transaction = self.model_to_entity(transaction) # try to replace with 
        return pp_transaction

class Updater(DB_Transaction):
    selector_class = Selector
    
     @staticmethod
     def get_transaction_by_id():
        transaction = self.ModelClass.objects.get(id=transaction_id)
        pp_transaction = self.model_to_entity(transaction) # try to replace with 
        return pp_transaction
                

'''

class DB_Creator:

    @staticmethod
    def create_payment_system_transaction(**kwargs):
        user = users_db_interface.DB_Selector.get_user_by_id(kwargs.get('user'))
        kwargs['user'] = user
        ps_transaction = PaymentSystemTransaction.objects.create(**kwargs)
        return ps_transaction

    @staticmethod
    def create_pp_transaction(**kwargs):
        pp_transaction = Transaction.objects.create(**kwargs)
        return pp_transaction


class DB_Updater:

    @staticmethod
    def update_payment_transaction_status(order_id, capture_id, status)->PaymentSystemTransaction:
        updated_count = PaymentSystemTransaction.objects.filter(order_id=order_id)\
            .update(status=status, capture_id = capture_id)
        payment_system_transaction = DB_Selector.get_payment_transaction_by_order_id(order_id)
        return payment_system_transaction



class DB_Deleter:
    pass


class DB_Selector:

    @staticmethod
    def get_payment_transaction_by_order_id(order_id) -> PaymentSystemTransaction:
        ps_transaction = PaymentSystemTransaction.objects.get(order_id=order_id)
        return ps_transaction

    @staticmethod
    def get_uncaptured_payments():
        uncaptured_orders = PaymentSystemTransaction.objects.filter(capture_id__isnull=True)
        return uncaptured_orders