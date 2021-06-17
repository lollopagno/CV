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
    """
