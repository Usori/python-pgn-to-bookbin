import chess
import chess.pgn
import struct
import chess.polyglot

# Função para gerar hash do tabuleiro usando Zobrist hashing
def get_zobrist_key(board):
    return chess.polyglot.zobrist_hash(board)

# Função para codificar um movimento no formato Polyglot
def encode_move(move):
    return chess.polyglot.encode_move(move)

# Função para adicionar uma entrada no livro Polyglot
def add_entry(book_file, board, move, weight=1, learn=0):
    key = get_zobrist_key(board)
    move_polyglot = encode_move(move)
    
    # Estrutura binária de uma entrada Polyglot: chave (8 bytes), movimento (2 bytes), peso (2 bytes), learn (2 bytes)
    entry = struct.pack(">QHHHHI", key, move_polyglot, weight, learn, 0, 0)
    book_file.write(entry)

# Função para processar o arquivo PGN e gerar o livro .bin
def pgn_to_polyglot(pgn_file, output_bin_file):
    with open(output_bin_file, "wb") as book:
        # Abrir o arquivo PGN
        with open(pgn_file) as pgn:
            # Carregar cada jogo do arquivo PGN
            while True:
                game = chess.pgn.read_game(pgn)
                if game is None:
                    break  # Se não houver mais jogos, parar o loop

                board = game.board()  # Inicializa o tabuleiro

                for node in game.mainline():  # Itera sobre as jogadas e nós
                    move = node.move
                    # Extrair o comentário se houver
                    comment = node.comment.strip()

                    # Tentar converter o comentário em weight, se possível
                    try:
                        weight = int(comment)  # Se o comentário for um número, usar como weight
                    except ValueError:
                        weight = 1  # Se não for numérico, usar weight padrão

                    # Adiciona a entrada no arquivo .bin
                    add_entry(book, board, move, weight)
                    board.push(move)  # Aplica o movimento no tabuleiro

# Caminho para o arquivo PGN de entrada e o arquivo .bin de saída
input_pgn_file = "partidas_comentadas.pgn"  # Substitua pelo seu arquivo PGN
output_bin_file = "meu_book_comentado.bin"  # Arquivo Polyglot .bin gerado

# Executar a conversão
pgn_to_polyglot(input_pgn_file, output_bin_file)

print("Livro de abertura Polyglot gerado com sucesso com base nos comentários do PGN!")
