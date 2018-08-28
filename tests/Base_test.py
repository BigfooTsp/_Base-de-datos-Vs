################################################################################
#		Base de Datos                        								   #
# 		básica para test												   #
################################################################################
from BBDD_2 import BBDD_Field_Element, BBDD_Field, BBDD_Base, BBDD_Operator



class Campo2(BBDD_Field):
    None


class BaseDatos(BBDD_Base):
    None



def main():
    op = BBDD_Operator()
    print(op.com.command_help())


if __name__ == '__main__':
	main()