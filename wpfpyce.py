class Move:
    def __init__(self, moveData, isEnpassant=False):
        g={1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h'}
        self.moveData=moveData
        self.isEnpassant=isEnpassant
        try:
            self.uci=f"{g[moveData[0][1]+1]}{9-(moveData[0][0]+1)}{g[moveData[1][1]+1]}{9-(moveData[1][0]+1)}"
        except:
            pass
        
    def __eq__(self, other):
        return other.uci == self.uci
    
class Piece:
    def __init__(self, pieceStr):
        self.piece=pieceStr
        self.col=pieceStr[0]
        self.pieceType=pieceStr[1].lower() if self.col=='b' else pieceStr[1].upper()
    def __repr__(self):
        return self.piece
    def __eq__(self, other):
        return self.piece==other.piece
class LegalMoveGenerator:
    def __init__(self,board):
        self.legalMoves=[]
        self.doublePawnPush=[6,1]
        self.colortoPlay="w"
        self.attackSquares=[]
        self.white_castlingrights=['O-O-O','O-O']
        self.black_castlingrights=['O-O-O','O-O']

        self.whiteEP=[]
        self.blackEP=[]
        
        
    def generateMoves(self, board):
        self.legalMoves=[]
        self.attackSquares=[]
        self.curBoard=board
        for x in range(8):
            for y in range(8):
                piece=self.curBoard[x][y]
                if piece.col!=self.colortoPlay:
                    continue
                self.generatePawnMoves(piece,[x,y])
                self.generateKingMoves(piece,[x,y])
                self.generateKnightMoves(piece,[x,y])
                self.generateQueenMoves(piece,[x,y])
                self.generateBishopMoves(piece,[x,y])
                self.generateRookMoves(piece,[x,y])
        return self.legalMoves
    def checkIfCanEnPassant(self, pos, list):
        
        for eP in list:
            if pos[0]==eP[0] and pos[1]==eP[1]:
                return True
        return False
    def generatePawnMoves(self, piece, pos):
        if piece.pieceType.lower()!="p":
            return      
        #:::black pawns:::#

        """
        DOUBLE PAWN PUSH
        """  

        if piece.col=='b':
            if pos[0]==self.doublePawnPush[1]:
                if self.curBoard[pos[0]+1][pos[1]].piece=="--":
                    if self.curBoard[pos[0]+2][pos[1]].piece=="--":
                        self.legalMoves.append(Move([tuple(pos),[pos[0]+2,pos[1]], piece, Piece('--')]))
                        self.attackSquares.append([pos[0]+2,pos[1]])
            if not pos[0]+1 > 7:
                if self.curBoard[pos[0]+1][pos[1]].piece=="--":
                        self.legalMoves.append(Move([tuple(pos),[pos[0]+1,pos[1]], piece, Piece('--')]))
                        self.attackSquares.append([pos[0]+1,pos[1]])
                if not pos[1]+1 > 7:
                    if self.curBoard[pos[0]+1][pos[1]+1].piece!="--":
                        if self.curBoard[pos[0]+1][pos[1]+1].col!=piece.col:
                            self.legalMoves.append(Move([tuple(pos),[pos[0]+1,pos[1]+1], piece,self.curBoard[pos[0]+1][pos[1]+1] ]))
                            self.attackSquares.append([pos[0]+1,pos[1]+1])
                    elif self.checkIfCanEnPassant(pos, self.blackEP):
                        self.legalMoves.append(Move([pos,[pos[0]+1,pos[1]+1]], True))
                        self.attackSquares.append([pos[0]+1,pos[1]+1])  
                if not pos[1]-1 < 0:
                    if self.curBoard[pos[0]+1][pos[1]-1].piece!="--":
                        if self.curBoard[pos[0]+1][pos[1]-1].col!=piece.col:
                            self.legalMoves.append(Move([tuple(pos),[pos[0]+1,pos[1]-1], piece,self.curBoard[pos[0]+1][pos[1]-1] ]))
                            self.attackSquares.append([pos[0]+1,pos[1]-1])     
                    elif self.checkIfCanEnPassant(pos, self.blackEP):
                        self.legalMoves.append(Move([pos,[pos[0]+1,pos[1]-1]], True))
                        self.attackSquares.append([pos[0]+1,pos[1]-1])   
            
        
        #:::white pawns:::#

        """
        DOUBLE PAWN PUSH
        """  
        if piece.col=='w':
            if pos[0]==self.doublePawnPush[0]:
                if self.curBoard[pos[0]-1][pos[1]].piece=="--":
                    if self.curBoard[pos[0]-2][pos[1]].piece=="--":
                        self.legalMoves.append(Move([tuple(pos),[pos[0]-2,pos[1]], piece, Piece('--')]))
                        self.attackSquares.append([pos[0]-2,pos[1]])
            if not pos[0]-1 < 0:
                if self.curBoard[pos[0]-1][pos[1]].piece=="--":
                        self.legalMoves.append(Move([tuple(pos),[pos[0]-1,pos[1]], piece, Piece('--')]))
                        self.attackSquares.append([pos[0]-1,pos[1]])
                if not pos[1]+1 > 7:
                    if self.curBoard[pos[0]-1][pos[1]+1].piece!="--":
                        if self.curBoard[pos[0]-1][pos[1]+1].col!=piece.col:
                            self.legalMoves.append(Move([tuple(pos),[pos[0]-1,pos[1]+1], piece,self.curBoard[pos[0]-1][pos[1]+1] ]))
                            self.attackSquares.append([pos[0]-1,pos[1]+1])

                    elif self.checkIfCanEnPassant(pos, self.whiteEP):
                        self.legalMoves.append(Move([pos,[pos[0]-1,pos[1]+1]], True))
                        self.attackSquares.append([pos[0]-1,pos[1]+1])
                if not pos[1]-1 < 0:
                    if self.curBoard[pos[0]-1][pos[1]-1].piece!="--":
                        if self.curBoard[pos[0]-1][pos[1]-1].col!=piece.col:
                            self.legalMoves.append(Move([tuple(pos),[pos[0]-1,pos[1]-1], piece,self.curBoard[pos[0]-1][pos[1]-1] ]))
                            self.attackSquares.append([pos[0]-1,pos[1]-1]) 
                    elif self.checkIfCanEnPassant(pos, self.whiteEP):
                        self.legalMoves.append(Move([pos,[pos[0]-1,pos[1]-1]], True))
                        self.attackSquares.append([pos[0]-1,pos[1]-1]) 

    def generateKingMoves(self, piece, pos):
        if piece.pieceType.lower()!="k":
            return
        for dir in [(1,0),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1),(0,-1),(0,1)]:
            newposx=pos[0]+dir[0]
            newposy=pos[1]+dir[1]
            if 0>newposy or 7<newposy:
                continue
            if 0>newposx or 7<newposx:
                continue

            if self.curBoard[newposx][newposy].piece=='--':
                self.legalMoves.append(Move([tuple(pos), [newposx,newposy], piece, Piece('--')]))
                self.attackSquares.append([newposx, newposy])
            elif self.curBoard[newposx][newposy].col==piece.col:
                continue
            elif self.curBoard[newposx][newposy].col!=piece.col:
                self.attackSquares.append([newposx, newposy])
                self.legalMoves.append(Move([tuple(pos), [newposx,newposy], piece, self.curBoard[newposx][newposy]]))
    def generateKnightMoves(self, piece, pos):
        if piece.pieceType.lower()!="n":
            return
        for dir in [(-2,1),(-2,-1),(2,-1),(2,1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            try:
                newposx=pos[0]+dir[0]
                newposy=pos[1]+dir[1]

                if 0>newposy or 7<newposy:
                    continue
                if 0>newposx or 7<newposx:
                    continue
                if self.curBoard[newposx][newposy].piece=='--':
                    self.legalMoves.append(Move([tuple(pos), [newposx,newposy], piece, Piece('--')]))
                    self.attackSquares.append([newposx, newposy])
                elif self.curBoard[newposx][newposy].col==piece.col:
                    continue
                elif self.curBoard[newposx][newposy].col!=piece.col:
                    self.attackSquares.append([newposx, newposy])
                    self.legalMoves.append(Move([tuple(pos), [newposx,newposy], piece, self.curBoard[newposx][newposy]]))
            except IndexError:
                continue
    def generateQueenMoves(self, piece, pos):
        if piece.pieceType.lower()!='q':return
        row=pos[0]
        col=pos[1]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),(1, 1), (-1, -1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                cpiece=self.curBoard[r][c]
                
                
                if cpiece.col!=piece.col:
                    if cpiece.piece=="--":
                        self.legalMoves.append(Move([tuple(pos), [r,c],piece,cpiece]))
                        self.attackSquares.append([r,c])
                        continue
                    self.legalMoves.append(Move([tuple(pos), [r,c],piece,cpiece]))
                    self.attackSquares.append([r,c])
                    break
                elif cpiece.col==piece.col:
                    break
    def generateRookMoves(self, piece, pos):
        if piece.pieceType.lower()!="r":
            return
        row=pos[0]
        col=pos[1]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                cpiece=self.curBoard[r][c]
                
                if cpiece.piece=="--":
                    self.legalMoves.append(Move([tuple(pos), [r,c],piece,cpiece]))
                    self.attackSquares.append([r,c])
                    continue
                elif cpiece.col!=piece.col:
                    self.legalMoves.append(Move([tuple(pos), [r,c],piece,cpiece]))
                    self.attackSquares.append([r,c])
                    break
                elif cpiece.col==piece.col:
                    break
                

    def generateBishopMoves(self, piece, pos):
        if piece.pieceType.lower()!="b":
            return
        row=pos[0]
        col=pos[1]
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                cpiece=self.curBoard[r][c]
                
                if cpiece.piece=="--":
                    self.legalMoves.append(Move([tuple(pos), [r,c],piece,cpiece]))
                    self.attackSquares.append([r,c])
                    continue
                elif cpiece.col!=piece.col:
                    self.legalMoves.append(Move([tuple(pos), [r,c],piece,cpiece]))
                    self.attackSquares.append([r,c])
                    break
                elif cpiece.col==piece.col:
                    break


    def __repr__(self):
        d=''
        for move in self.legalMoves:
            d+=f'{move.uci}{move.moveData[0]}{move.moveData[1]}\n'
        return f'{d}{len(self.legalMoves)}'  
class Board:
    def __init__(self):
        self.BoardStr=[["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bP","bP","bP","bP","bP","bP","bP","bP"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        
        self.Board=[]
        self.kSP=((0,4),(7,4))
        for y in range(8):
            self.Board.append([])
            for x in range(8):
                self.Board[y].append(Piece(self.BoardStr[y][x]))
        self.LegalMoveGenerator=LegalMoveGenerator(self.Board)
        self.moveLog=[]
    def checkIfKingCanCastle(self, long=False, Color='w'):
        castling={'w':self.LegalMoveGenerator.white_castlingrights,
                  'b':self.LegalMoveGenerator.black_castlingrights}
        kSP=self.kSP[1] if Color=="w" else self.kSP[0]
        rank=0 if Color=='b' else 7
        if {False:"O-O",True:"O-O-O"}[long] not in castling[Color]:
            print('does not have castling rights')
            return False
        if self.Board[kSP[0]][kSP[1]].piece!=Piece(f'{Color}K').piece:
            print('king not in startingposition')
            print(self.Board[kSP[0]][kSP[1]])
            return False
        if long:
            for i in range(1,4,1):
                if self.Board[rank][i+2].piece not in(Piece('--').piece, Piece(f'{Color}K').piece):
                    print(rank, i+2)
                    print(self.Board[rank][i+2])
                    return False
            else:
                return True
        else:
            for i in range(2):
                if self.Board[rank][i+5].piece!=Piece('--').piece:
                    return False
            else:
                return True

    def validUci(self,uci):
        uciToRC={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        
        start=[8-int(uci[1]),uciToRC[uci[0]]]
        for move in self.LegalMoveGenerator.legalMoves:
            if move.isEnpassant:
                if start==move.moveData[0]:
                    return (True,'f')
                return (False,'t')
            if move.uci == uci:
                return (True,'t')
        return (False, 't')
    def indangersKing(self, uci):
        isAttacked=False
        uciToRC = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        start = (8 - int(uci[1]), uciToRC[uci[0]])
        if self.validUci(uci)[1] == 't':
            end = (8 - int(uci[3]), uciToRC[uci[2]])
        else:
            end = (9 - int(uci[3]), uciToRC[uci[2]])
        piece = self.Board[start[0]][start[1]]
        captured_piece = self.Board[end[0]][end[1]]
        self.Board[end[0]][end[1]] = piece
        self.Board[start[0]][start[1]] = Piece('--')

        attacker_color = 'b' if piece.col == 'w' else 'w'
        self.LegalMoveGenerator.colortoPlay=attacker_color

        self.LegalMoveGenerator.generateMoves(self.Board)

        for move in self.LegalMoveGenerator.legalMoves:
            if move.moveData[3].pieceType.lower()=='k':
                isAttacked=True
        self.Board[start[0]][start[1]] = piece
        self.Board[end[0]][end[1]] = captured_piece
        self.LegalMoveGenerator.colortoPlay='b' if attacker_color == 'w' else 'w'
        self.LegalMoveGenerator.generateMoves(self.Board)

        return isAttacked

    def push_uci(self, uci):
        rank=0 if self.LegalMoveGenerator.colortoPlay=='b' else 7
        if uci in ['O-O-O',"O-O"]:
            if self.checkIfKingCanCastle({"O-O-O":True, "O-O":False}[uci], self.LegalMoveGenerator.colortoPlay):
                if uci=="O-O-O":
                    self.Board[rank][0]=Piece('--')
                    self.Board[rank][3]=Piece(f'{self.LegalMoveGenerator.colortoPlay}R')
                    self.Board[rank][2]=Piece(f'{self.LegalMoveGenerator.colortoPlay}K')
                    self.Board[rank][4]=Piece('--')
                    return
                else:
                    self.Board[rank][7]=Piece('--')
                    self.Board[rank][5]=Piece(f'{self.LegalMoveGenerator.colortoPlay}R')
                    self.Board[rank][6]=Piece(f'{self.LegalMoveGenerator.colortoPlay}K')
                    self.Board[rank][4]=Piece('--')
                    return
            else:
                return print('Cannot Castle')

        self.LegalMoveGenerator.generateMoves(self.Board)
        
        if not self.validUci(uci)[0]:
            return print('invalid')
        if self.indangersKing(uci):
            return print('psuedolegal')
        uciToRC={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        self.LegalMoveGenerator.whiteEP=[]
        self.LegalMoveGenerator.blackEP=[]
        start=(8-int(uci[1]),uciToRC[uci[0]])
        if self.validUci(uci)[1]=='t':
            end=(8-int(uci[3]),uciToRC[uci[2]])
        else:
            end=(9-int(uci[3]),uciToRC[uci[2]])
        endpiece=self.Board[end[0]][end[1]]
        piece=self.Board[start[0]][start[1]]
        bcr=self.LegalMoveGenerator.black_castlingrights
        wcr=self.LegalMoveGenerator.white_castlingrights
        if endpiece.piece[1]=='R':
            if endpiece.col=='b':
                bcrRight={0:bcr[0],7:bcr[1]}[end[1]]
                bcr.remove(bcrRight)
            else:
                wcrRight={0:wcr[0],7:wcr[1]}[end[1]]
                wcr.remove(wcrRight)
        if piece.piece[1]=='P':
            gg=''
            if piece.col=='b':
                if end[0]==7:
                    while gg not in ["q",'b','n','r']:
                        gg=input('Promote Pawn (Q/B/N/R): ').lower()
                        print('invalid piece')
                    piece=Piece(f"b{gg.upper()}")
                if end[0]==3:
                    self.LegalMoveGenerator.whiteEP.append((end[0], end[1]+1))
                    self.LegalMoveGenerator.whiteEP.append((end[0], end[1]-1))
            else:
                if end[0]==4:
                    self.LegalMoveGenerator.whiteEP.append((end[0], end[1]+1))
                    self.LegalMoveGenerator.whiteEP.append((end[0], end[1]-1))
                if end[0]==0:
                    while gg not in ["q",'b','n','r']:
                        gg=input('Promote Pawn (Q/B/N/R): ').lower()
                        print('invalid piece')
                    piece=Piece(f"w{gg.upper()}")
                    
        if piece.piece[1]=='K':
            if piece.col=='b':
                self.LegalMoveGenerator.black_castlingrights=[]
            else:
                self.LegalMoveGenerator.white_castlingrights=[]
        if piece.piece[1]=='R':
            if piece.col=='b':
                if start[1]==0:
                    g=self.LegalMoveGenerator.black_castlingrights[0]
                    self.LegalMoveGenerator.black_castlingrights.remove(g)
                else:
                    g=self.LegalMoveGenerator.black_castlingrights[1]
                    self.LegalMoveGenerator.black_castlingrights.remove(g)
            else:
                if start[1]==0:
                    g=self.LegalMoveGenerator.white_castlingrights[0]
                    self.LegalMoveGenerator.white_castlingrights.remove(g)
                else:
                    g=self.LegalMoveGenerator.white_castlingrights[1]
                    self.LegalMoveGenerator.white_castlingrights.remove(g)
        self.moveLog.append(Move([start, end, piece,self.Board[end[0]][end[1]]]))
        self.Board[end[0]][end[1]]=piece
        self.Board[start[0]][start[1]]=Piece('--')

        self.LegalMoveGenerator.colortoPlay='b' if self.LegalMoveGenerator.colortoPlay=='w' else 'w'

    def __repr__(self):
        d=''
        for rank in self.Board:
            for pieces in rank:
                d=d+f' {pieces.pieceType} 'if pieces.pieceType!="-" else d+" . "
            d+='\n'
        return d
ChessBoard=Board()
