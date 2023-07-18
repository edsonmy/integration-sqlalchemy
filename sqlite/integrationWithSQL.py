# Integração com SQLITE

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DECIMAL
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(9))

    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    saldo = Column(DECIMAL, default=0)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"

# conexão com o banco de dados
engine = create_engine("sqlite:///bank.db")

# criando as classes como tabelas
Base.metadata.create_all(engine)

with Session(engine) as session:
    maria = Cliente(
        nome='Maria',
        cpf='123456789',
        endereco='ABCDE',
        conta=[Conta(
            tipo='CC',
            agencia='0001',
            num=1,
            saldo=100
        ), Conta(
            tipo='POUP',
            agencia='0001',
            num=1902,
            saldo=140
        )]
    )

    jose = Cliente(
        nome='Jose',
        cpf='987654321',
        endereco='EDFGR',
        conta=[Conta(
            tipo='CC',
            agencia='0001',
            num=2,
            saldo=10
        )]
    )


    # gravar no BD
    session.add_all([maria, jose])

    session.commit()


cmd = select(Cliente).where(Cliente.nome.in_(["Maria", 'Jose']))
print('Recuperando clientes com filtro')
for cliente in session.scalars(cmd):
    print(cliente)

cmd_conta = select(Conta).where(Conta.id_cliente.in_([1]))
print('\nRecuperando contas do cliente 1')
for conta in session.scalars(cmd_conta):
    print(conta)


cmd_order = select(Cliente).order_by(Cliente.nome.desc())
print("\nRecuperando cliente ordenado")
for result in session.scalars(cmd_order):
    print(result)

cmd_join = select(Cliente.nome, Conta.agencia, Conta.num).join_from(Cliente, Conta)
print("\nRecuperando cliente x conta (não funciona)")
for result in session.scalars(cmd_join):
    print(result)


connection = engine.connect()
results = connection.execute(cmd_join).fetchall()
print("\nExecutando a partir da connection")
for result in results:
    print(result)

cmd_count = select(func.count('*')).select_from(Cliente)
print('\nTotal de instâncias em Cliente')
for result in session.scalars(cmd_count):
    print(result)

# encerrando de fato a session
session.close()

