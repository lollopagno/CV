def findChessboardCorners(img, pattern_size, flag):
    r"""
    Trova le posizioni dei corner interni alla scacchiera con i quadrati.

    :param img: immagine di input in grayscale.
    :param pattern_size: numero di corners interni per riga e colonna della scacchiera.
    :param flag: flag per introdurre la soglia adattativa, normalizzare la gamma, .. ecc

    @return:    ret: true se ha identificato tutti i corners della scacchiera, false altrimenti.
                corners: array dei corners individuati.
    """


def findCirclesGrid(img, pattern_size, flag):
    r"""
    Analoga alla funzione @findChessboardCorners applicabile ad una scacchiera con i cerchi.
    """


def drawChessboardCorners(img, patter_size, corners, patter_was_found):
    r"""
    Disegna i corners individuati. La funzione disegna singoli corners della scacchiera rilevati come cerchi rossi se la
    scacchiera non è stata trovata o come corners colorati collegati con le linee se la scacchiera è stata trovata.

    :param img: immagine in cui disegnare i corners.
    :param patter_size: numero di corners interni per riga e colonna della scacchiera.
    :param corners: corners individuati da @findChessboardCorners o da @findCirclesGrid.
    :param patter_was_found: parametro che indica se la scacchiera completa è stata trovata o meno
    (è il ret di return di @findChessboardCorners o @findCirclesGrid).
    """


def calibrateCamera(obj_points, image_points, size, flag, criteria):
    r"""
    Trova i parametri intrinseci ed estrinseci della camera a partire dal pattern della schacchiera.

    :param obj_points: punti oggetto nello spazio del mondo reale.
    :param image_points: punti immagine proiettati.
    :param size: dimensione dell'immagine (non dimensione della schacchiera!!).
    :param flag: flag per settaggio della calibrazione.
    :param criteria: criterio di terminazione per l'algoritmo di ottimizzazione iterativa.

    @return:    ret: boolean.
                camera_matrix: matrice intrinseca della camera.
                coeff_dist: coefficienti di distorsione.
                rvec: coefficienti di rotazione.
                tvec: coefficienti di traslazione.
    """


def cornerSubPix(img, corner, win_size, zero_zone, criteria):
    r"""
    Perfeziona le posizioni dei corners del pattern.
    La funzione itera per trovare la posizione accurata dei sotto-pixel dei corner o punti di sella radiali.

    :param img: immagine di input in grayscale.
    :param corner: coordinate iniziali dei corners individuati (di solito dalla funzione findChessboardCorners).
    :param win_size: metà della lunghezza laterale della finestra di ricerca.
                     Se la finestra è 5 x 5 = (5*2+1) x (5*2+1) = 11 x 11
    :param zero_zone:
    :param criteria: criteri per la terminazione del processo iterativo di perfezionamento dei corners.

    @return: posizioni accurate dei corners del pattern.
    """


def solvePnP(obj_points, image_points, camera_matrix, coeff_dist, flag):
    r"""
    Trova un oggetto 'posa' da corrispondenze di punti 2D/3D.

    :param obj_points: punti oggetto 3D nello spazio del mondo reale.
    :param image_points: punti 2D dell'immagine planare (rappresentano i corner restituiti da @cornerSubPix).
    :param camera_matrix: matrice intriseca della telecamera.
    :param coeff_dist: coefficienti di distorsione.
    :param flag: flag per risolvere il problema PnP.

    @return:    ret: true se ha identificato tutti i corners della scacchiera, false altrimenti.
                rvec: coefficienti di rotazione.
                tvec: coefficienti di traslazione.
    """


def projectPoints(obj_points, rvec, tvec, camera_matrix, coeff_dist):
    r"""
    Proietta i punti 3D in un immagine planare.

    :param obj_points: punti oggetto.
    :param rvec: coefficienti di rotazione.
    :param tvec: coefficienti di traslazione.
    :param camera_matrix: matrice intriseca della telecamera.
    :param coeff_dist: coefficienti di distorsione.

    @return     img_point: array di punti immagine.
                jacobian: (output opzionale), matrice jacobiana delle derivate dei punti immagine.
    """
    pass


def undistort(img, camera_matrix, coeff_dist, new_camera_matrix):
    r"""
    Esegue una trasformazione sull'immagine per compensare la distorsione (radiale e tangenziale) della lente.
    Quei pixel nell'immagine di output, per i quali non ci sono pixel corrispondenti nell'immagine di input,
    sono riempiti con zeri (colore nero).

    :param img: immagine di input (RGB).
    :param camera_matrix: matrice intriseca della telecamera.
    :param coeff_dist: coefficienti di distorsione.
    :param new_camera_matrix: Matrice della fotocamera dell'immagine distorta. Di default, è lo stesso di cameraMatrix,
    ma è possibile ridimensionare e spostare ulteriormente il risultato utilizzando una matrice diversa.
    """


def rodrigues(matrix):
    r"""
    Converte una matrice di rotazione (3x3) in un array di rotazione (3x1, 1x3) o viceversa.

    :param matrix: matrice o array da convertire.

    @return     matrice o array convertito.
    """


def getPerspectiveTransform(src, dst):
    r"""
    Calcola una trasformazione prospettica da quattro coppie dei punti corrispondenti.

    :param src: coordinate dei vertici corrispondenti all'immagine originale.
    :param dst: coordinate dei vartici corrispondenrti all'immagine di output.

    @return     M: matrice prospettica dei vertici.
    """


def warpPerspective(src, M, size, flags, border_mode, border_value):
    r"""
    Applica la trasformazione prospettica ad un immagine.

    :param src: immagine di input
    :param M: matrice di trasformazione
    :param size: dimensione dell'immagine di output.
    :param flags: tipo di interpolazione da eseguire
    :param border_mode: metodo di estrapolazione dei pixels
    :param border_value: usato in caso di bordi costanti.

    @return     warper: immagine di output a cui è stata applicata la trasformazione.
    """

def findHomography(src_points, dst_points, method, ransac, max_iter, confidence):
    r"""
    Trova la trasformazione prospettica tra due piani.

    :param src_points: coordinate dei punti del piano di input.
    :param dst_points: coordinate dei punti del piano target.
    :param method: metodo usato per calcolare la matrice omografica.
    :param ransac: Massimo errore di retroprograzione permesso (utilizzato con RANSAC).
    :param max_iter: numero massimo di iterazioni RANSAC.
    :param confidence: livello di confidenza compreso tra 0 e 1.

    @return Trasformazione prospettica.
    """