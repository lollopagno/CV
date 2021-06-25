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


def calcOpticalFlowFarneback(prev, next, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags):
    r"""
    Calcola il flusso ottico denso usando l'algoritmo di Gunnar Farneback.

    :param prev: frame precedente dell'immaggine
    :param next: frame corrente
    :param pyr_scale: scala dell'immagine per creare piramidi per ogni immagine.
    :param levels: numero di livelli piramidali. Con levels=1 non vengono creati livelli aggiuntivi.
    :param winsize: Dimensione della finestra.
    :param iterations: numero di iterazioni che l'algoritmo fa ad ogni livello piramidale.
    :param poly_n: dimensione dei pixel vicini usati per trovare l'espansione polinomiale per ogni pixel.
    :param poly_sigma: deviazione standard della curca Gaussiana
    :param flags: tipologie di operazioni disponibili da applicare (OPTFLOW_USE_INITIAL_FLOW , OPTFLOW_FARNEBACK_GAUSSIAN)

    @return     flow: immagine di flusso di output calcolata aventi le stesse dimensioni di @prev.
    """


def calcOpticalFlowPyrLK(prev, next, prevPts, nextPts, winSize, maxLevel, criteria, flags, minEigThreshold):
    r"""
    Calcola il flusso ottico per un set di feature sparse usando il metodo iterativo Lucas-Kanade con piramidi.

    :param prev: immagine di input precedente.
    :param next: immagine corrente.
    :param prevPts: punti associati all'immagine @prev.
    :param nextPts: punti associati all'immagine @next
    :param winSize: dimensione della finestra di ricerca.
    :param maxLevel: numero di livelli piramidali massimi.
    :param criteria: criteri di terminazione dell'algortimo.
    :param flags: tipologie di operazioni disponibili da applicare (OPTFLOW_USE_INITIAL_FLOW , OPTFLOW_LK_GET_MIN_EIGENVALS)

    @return     p1: nuove posizioni calcolate dalle features di input.
                status: stato dell'output. Con status = 1, il flusso ottico è stato trovato, altrimenti status = 0.
                error: errore dell'output.
    """
    pass
<<<<<<< Updated upstream


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

def calcOpticalFlowFarneback(prev, next, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags):
    r"""
    Calcola il flusso ottico denso usando l'algoritmo di Gunnar Farneback.

    :param prev: frame precedente dell'immaggine
    :param next: frame corrente
    :param pyr_scale: scala dell'immagine per creare piramidi per ogni immagine.
    :param levels: numero di livelli piramidali. Con levels=1 non vengono creati livelli aggiuntivi.
    :param winsize: Dimensione della finestra.
    :param iterations: numero di iterazioni che l'algoritmo fa ad ogni livello piramidale.
    :param poly_n: dimensione dei pixel vicini usati per trovare l'espansione polinomiale per ogni pixel.
    :param poly_sigma: deviazione standard della curca Gaussiana
    :param flags: tipologie di operazioni disponibili da applicare (OPTFLOW_USE_INITIAL_FLOW , OPTFLOW_FARNEBACK_GAUSSIAN)

    @return     flow: immagine di flusso di output calcolata aventi le stesse dimensioni di @prev.
    """


def calcOpticalFlowPyrLK(prev, next, prevPts, nextPts, winSize, maxLevel, criteria, flags, minEigThreshold):
    r"""
    Calcola il flusso ottico per un set di feature sparse usando il metodo iterativo Lucas-Kanade con piramidi.

    :param prev: immagine di input precedente.
    :param next: immagine corrente.
    :param prevPts: punti associati all'immagine @prev.
    :param nextPts: punti associati all'immagine @next
    :param winSize: dimensione della finestra di ricerca.
    :param maxLevel: numero di livelli piramidali massimi.
    :param criteria: criteri di terminazione dell'algortimo.
    :param flags: tipologie di operazioni disponibili da applicare (OPTFLOW_USE_INITIAL_FLOW , OPTFLOW_LK_GET_MIN_EIGENVALS)

    @return     p1: nuove posizioni calcolate dalle features di input.
                status: stato dell'output. Con status = 1, il flusso ottico è stato trovato, altrimenti status = 0.
                error: errore dell'output.
    """
    pass
=======
>>>>>>> Stashed changes
