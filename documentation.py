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


def getOptimalNewCameraMatrix(camera_matrix, coeff_dist, image_size, alpha, new_image_size):
    r"""
    Ritorna una nuova matrice intrinseca della fotocamera in base al parametro alpha.

    :param camera_matrix: matrice intriseca della telecamera.
    :param coeff_dist: coefficienti di distorsione.
    :param image_size: dimensione dell'immagine originale.
    :param alpha: parametro di ridimensionamento compreso tra 0 (quando tutti i pixel nell'immagine non distorta sono validi)
     e 1 (quando tutti i pixel dell'immagine originale vengono mantenuti nell'immagine non distorta).
    :param new_image_size: dimensione dell'immagine dopo la rettifica. Di default è settato a image_size

    @return     new_camera_matrix: nuova matrice intrinseca della fotocamera.
                roi: area di tutti i pixel nell'immagine non distorta.
    """


def rodrigues(matrix):
    r"""
    Converte una matrice di rotazione (3x3) in un array di rotazione (3x1, 1x3) o viceversa.

    :param matrix: matrice o array da convertire.

    @return     matrice o array convertito.
    """


def StereoSGBM_create(min_disparity, num_disparities, block_size, P1, P2, disp_12_max_diff, pre_filter_cap,
                      uniqueness_radio, speckle_win_size, speckle_range):
    r"""
    Crea un oggettto stereo SGBM.

    :param min_disparity: Valore di disparità minimo tra le due immagini.
    :param num_disparities: Differenza tra la dispartià massima e quella minima. Deve essere un valore > 0, divisibile per 16.
    :param block_size: Dimensione del blocco di match. Deve essere un valore >= 1, dispari.
    :param P1: parametro che controlla l'uniformità della disparità. Tale parametro indica la penalità
    sulla variazione di disparità di più o meno 1 tra i pixel vicini.
    :param P2: parametro che controlla l'uniformità della disparità. P2 > P1. Tale parametro indica la penalità
    sulla variazione di disparità di più di 1 tra pixel vicini.
    :param disp_12_max_diff: Differenza massima consentita.
    :param pre_filter_cap: Valore di troncamento per i pixel dell'immagine prefiltrati.
    :param uniqueness_radio:
    :param speckle_win_size: Massima dimensione di smooth delle regioni di disparità da considerare.
    :param speckle_range: Massima variazione di disparità all'interno di ciascun componente connesso.

    @return oggetto stereo SGBM.
    """


def findFundamentalMat(points_1, points_2, method, ransac_threshold, confidence, max_iters):
    r"""
    Calcola la matrice fondamentale a partire dai punti delle due immagini.

    :param points_1: punti della prima immagine.
    :param points_2: punti della seconda immagine.
    :param method: intero che indica il tipo di computazione per il calcolo della matrice.
    :param ransac_threshold: Parametro usato solo per RANSAC. Indica la massima distanza tra un punto a un linea epipolare
    in pixel, sopra il quale il punto è considerato un outlier e non usato per il calcolo della matrice.
    :param confidence: Parametro usato solo per RANSAC e LMedS. Specifica il livello di confidenza desiderato.
    :param max_iters: Numero massimo di iterazioni.

    @return     F: matrice fondamentale.
                mask: (Opzionale) maschera di output.
    """


def computeCorrespondEpilines(points, which_image, F):
    r"""
    Per ogni punto in un immagine, computa la corrispondente epilinea in un altra immagine.

    :param points: punti (matrice 1 x N o N x 1).
    :param which_image: Indice dell'immagine che contiene i punti.
    :param F: matrice essenziale.

    @return Vettore contenente le linee epipolari corrispondenti ai punti dell'altra immagine.
    Ogni linea è codifica da 3 punti (a, b, c) secondo l'equazione ax + by+ c = 0.
    """

def reprojectImageTo3D(disparity, Q, handle_missing_value, d_depth):
    r"""
    Riproietta un'immagine di disparità in un spazio 3D. La funzione trasforma una mappa di disparità a singolo canale
    in un'immagine a 3 canali che rappresenta la superficie 3D.

    :param disparity: immagine di input.
    :param Q: matrice di trasformazione proiettiva 4 X 4.
    :param handle_missing_value: Indica se la funziona deve gestire i valori mancanti
    (punti in cui la disparità non è stata calcolata). Se tale parametro è vero, i pixel con disparità
    minima, che corrispondono agli outlier, vengono trasformati in punti 3D con un valore Z molto grande.
    :param d_depth: profondità dell'arrray di output.

    @return Immagine delle stesse dimensioni di quella di input.
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