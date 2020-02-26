from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level
from skimage.draw import line, ellipse_perimeter, ellipse
import numpy as np

class Drawing:
    @staticmethod
    def draw_line(layer, p0, p1, tile):
        coords_y, coords_x = line(p0[0], p0[1], p1[0], p1[1])

        coords_y, coords_x =  Drawing._coords_inside_image(
            np.array(coords_y, dtype=np.intp),
            np.array(coords_x, dtype=np.intp),
            layer.shape)

        layer[coords_y, coords_x] = tile


    @staticmethod
    def draw_ellipse(layer, center, radius_y, radius_x, tile):
        coords_y, coords_x = ellipse_perimeter(center[0], center[1], radius_y, radius_x, 0., layer.shape)
        layer[coords_y, coords_x] = tile


    @staticmethod
    def fill_ellipse(layer, center, radius_y, radius_x, tile):
        coords_y, coords_x = ellipse(center[0], center[1], radius_y, radius_x, layer.shape)
        layer[coords_y, coords_x] = tile
        Drawing.draw_ellipse(layer, center, radius_y, radius_x, tile)


    @staticmethod
    def draw_rectangle(layer, p_min, p_max, tile):
        p_min, p_max = Drawing.ensure_max_min_correct(p_min, p_max)
        points = [(p_min[0], p_min[1]), (p_max[0], p_min[1]), (p_max[0], p_max[1]), (p_min[0], p_max[1])]
        for i in range(len(points)):
            Drawing.draw_line(layer, points[i - 1], points[i], tile)
        

    @staticmethod
    def fill_rectangle(layer, p_min, p_max, tile):
        p_min, p_max = Drawing.ensure_max_min_correct(p_min, p_max)
        for i in range(p_min[1], p_max[1] + 1):
            Drawing.draw_line(layer, (p_min[0], i), (p_max[0], i), tile)


    @staticmethod
    def ensure_max_min_correct(p_min, p_max):
        p_min2 = np.minimum(p_min, p_max)
        p_max2 = np.maximum(p_min, p_max)
        return p_min2, p_max2



    @staticmethod
    def _coords_inside_image(rr, cc, shape, val=None):
        """
        Return the coordinates inside an image of a given shape.
        Parameters
        ----------
        rr, cc : (N,) ndarray of int
            Indices of pixels.
        shape : tuple
            Image shape which is used to determine the maximum extent of output
            pixel coordinates.  Must be at least length 2. Only the first two values
            are used to determine the extent of the input image.
        val : (N, D) ndarray of float, optional
            Values of pixels at coordinates ``[rr, cc]``.
        Returns
        -------
        rr, cc : (M,) array of int
            Row and column indices of valid pixels (i.e. those inside `shape`).
        val : (M, D) array of float, optional
            Values at `rr, cc`. Returned only if `val` is given as input.
        """
        mask = (rr >= 0) & (rr < shape[0]) & (cc >= 0) & (cc < shape[1])
        if val is None:
            return rr[mask], cc[mask]
        else:
            return rr[mask], cc[mask], val[mask]