from dungeon_level.dungeon_tiles import Tiles
from dungeon_level.level import Level
import numpy as np
from PIL import ImageDraw

class Drawing:
    @staticmethod
    def draw_line(layer, p0, p1, tile):
        coords_y, coords_x = Drawing._line(p0[0], p0[1], p1[0], p1[1], layer.shape)
        layer[coords_y, coords_x] = tile


    @staticmethod
    def draw_ellipse(layer, center, radius_y, radius_x, tile):
        coords_y, coords_x = Drawing._ellipse_perimeter(center[0], center[1], radius_y, radius_x, 0., layer.shape)
        layer[coords_y, coords_x] = tile

    @staticmethod
    def draw_rectangle(layer, p_min, p_max, tile):
        points = [(p_min[0], p_min[1]), (p_max[0], p_min[1]), (p_max[0], p_max[1]), (p_min[0], p_max[1])]
        for i in range(len(points)):
            Drawing.draw_line(layer, points[i - 1], points[i], tile)




    # The methods that begin with underscore come from the skimage library.
    # https://github.com/scikit-image/scikit-image/blob/master/skimage/draw/_draw.pyx
    # We only need a couple methods for drawing shapes, so I didn't want to 
    # add the entire library# as a dependency.

    @staticmethod
    def _line(r0, c0, r1, c1, shape):
        """Generate line pixel coordinates.
        Parameters
        ----------
        r0, c0 : int
            Starting position (row, column).
        r1, c1 : int
            End position (row, column).
        Returns
        -------
        rr, cc : (N,) ndarray of int
            Indices of pixels that belong to the line.
            May be used to directly index into an array, e.g.
            ``img[rr, cc] = 1``.
        See Also
        --------
        line_aa : Anti-aliased line generator
        """
        steep = 0
        r = r0
        c = c0
        dr = abs(r1 - r0)
        dc = abs(c1 - c0)

        rr = np.zeros(max(dc, dr) + 1, dtype=np.intp)
        cc = np.zeros(max(dc, dr) + 1, dtype=np.intp)

        if (c1 - c) > 0:
            sc = 1
        else:
            sc = -1
        if (r1 - r) > 0:
            sr = 1
        else:
            sr = -1
        if dr > dc:
            steep = 1
            c, r = r, c
            dc, dr = dr, dc
            sc, sr = sr, sc
        d = (2 * dr) - dc

        for i in range(dc):
            if steep:
                rr[i] = c
                cc[i] = r
            else:
                rr[i] = r
                cc[i] = c
            while d >= 0:
                r = r + sr
                d = d - (2 * dc)
            c = c + sc
            d = d + (2 * dr)

        rr[dc] = r1
        cc[dc] = c1

        if shape is not None:
            return Drawing._coords_inside_image(np.array(rr, dtype=np.intp),
                                    np.array(cc, dtype=np.intp),
                                    shape)

        return np.array(rr, dtype=np.intp), np.array(cc, dtype=np.intp)

        return np.asarray(rr), np.asarray(cc)


    @staticmethod
    def _ellipse_perimeter(r_o, c_o, r_radius, c_radius, orientation, shape):
        """Generate ellipse perimeter coordinates.
        Parameters
        ----------
        r_o, c_o : int
            Centre coordinate of ellipse.
        r_radius, c_radius : int
            Minor and major semi-axes. ``(r/r_radius)**2 + (c/c_radius)**2 = 1``.
        orientation : double
            Major axis orientation in clockwise direction as radians.
        shape : tuple
            Image shape which is used to determine the maximum extent of output pixel
            coordinates. This is useful for ellipses that exceed the image size.
            If None, the full extent of the ellipse is used.
        Returns
        -------
        rr, cc : (N,) ndarray of int
            Indices of pixels that belong to the ellipse perimeter.
            May be used to directly index into an array, e.g.
            ``img[rr, cc] = 1``.
        References
        ----------
        .. [1] A Rasterizing Algorithm for Drawing Curves, A. Zingl, 2012
            http://members.chello.at/easyfilter/Bresenham.pdf
        """

        # If both radii == 0, return the center to avoid infinite loop in 2nd set
        if r_radius == 0 and c_radius == 0:
            return np.array(r_o), np.array(c_o)

        # Pixels
        rr = list()
        cc = list()

        # Compute useful values
        rd = r_radius * r_radius
        cd = c_radius * c_radius

        if orientation == 0:
            c = -c_radius
            r = 0
            e2 = rd
            err = c * (2 * e2 + c) + e2
            while c <= 0:
                # Quadrant 1
                rr.append(r_o + r)
                cc.append(c_o - c)
                # Quadrant 2
                rr.append(r_o + r)
                cc.append(c_o + c)
                # Quadrant 3
                rr.append(r_o - r)
                cc.append(c_o + c)
                # Quadrant 4
                rr.append(r_o - r)
                cc.append(c_o - c)
                # Adjust `r` and `c`
                e2 = 2 * err
                if e2 >= (2 * c + 1) * rd:
                    c += 1
                    err += (2 * c + 1) * rd
                if e2 <= (2 * r + 1) * cd:
                    r += 1
                    err += (2 * r + 1) * cd
            while r < r_radius:
                r += 1
                rr.append(r_o + r)
                cc.append(c_o)
                rr.append(r_o - r)
                cc.append(c_o)

        else:
            sin_angle = np.sin(orientation)
            za = (cd - rd) * sin_angle
            ca = np.sqrt(cd - za * sin_angle)
            ra = np.sqrt(rd + za * sin_angle)

            a = ca + 0.5
            b = ra + 0.5
            za = za * a * b / (ca * ra)

            ir0 = int(r_o - b)
            ic0 = int(c_o - a)
            ir1 = int(r_o + b)
            ic1 = int(c_o + a)

            ca = ic1 - ic0
            ra = ir1 - ir0
            za = 4 * za * np.cos(orientation)
            w = ca * ra
            if w != 0:
                w = (w - za) / (w + w)
            icd = int(np.floor(ca * w + 0.5))
            ird = int(np.floor(ra * w + 0.5))

            # Draw the 4 quadrants
            rr_t, cc_t = Drawing._bezier_segment(ir0 + ird, ic0, ir0, ic0, ir0, ic0 + icd, 1-w)
            rr.extend(rr_t)
            cc.extend(cc_t)
            rr_t, cc_t = Drawing._bezier_segment(ir0 + ird, ic0, ir1, ic0, ir1, ic1 - icd, w)
            rr.extend(rr_t)
            cc.extend(cc_t)
            rr_t, cc_t = Drawing._bezier_segment(ir1 - ird, ic1, ir1, ic1, ir1, ic1 - icd, 1-w)
            rr.extend(rr_t)
            cc.extend(cc_t)
            rr_t, cc_t = Drawing._bezier_segment(ir1 - ird, ic1, ir0, ic1, ir0, ic0 + icd,  w)
            rr.extend(rr_t)
            cc.extend(cc_t)

        if shape is not None:
            return Drawing._coords_inside_image(np.array(rr, dtype=np.intp),
                                    np.array(cc, dtype=np.intp),
                                    shape)

        return np.array(rr, dtype=np.intp), np.array(cc, dtype=np.intp)


    @staticmethod
    def _bezier_segment(r0, c0, r1, c1, r2, c2, weight):
        """Generate Bezier segment coordinates.
        Parameters
        ----------
        r0, c0 : int
            Coordinates of the first control point.
        r1, c1 : int
            Coordinates of the middle control point.
        r2, c2 : int
            Coordinates of the last control point.
        weight : double
            Middle control point weight, it describes the line tension.
        Returns
        -------
        rr, cc : (N,) ndarray of int
            Indices of pixels that belong to the Bezier curve.
            May be used to directly index into an array, e.g.
            ``img[rr, cc] = 1``.
        Notes
        -----
        The algorithm is the rational quadratic algorithm presented in
        reference [1]_.
        References
        ----------
        .. [1] A Rasterizing Algorithm for Drawing Curves, A. Zingl, 2012
            http://members.chello.at/easyfilter/Bresenham.pdf
        """
        # Pixels
        cc = list()
        rr = list()

        # Steps
        sc = c2 - c1
        sr = r2 - r1

        d2c = c0 - c2
        d2r = r0 - r2
        d1c = c0 - c1
        d1r = r0 - r1
        rc = d1c * sr + d1r * sc
        cur = d1c * sr - d1r * sc


        # If not a straight line
        if cur != 0 and weight > 0:
            if (sc * sc + sr * sr > d1c * d1c + d1r * d1r):
                # Swap point 0 and point 2
                # to start from the longer part
                c2 = c0
                c0 -= d2c
                r2 = r0
                r0 -= d2r
                cur = -cur
            d1c = 2 * (4 * weight * sc * d1c + d2c * d2c)
            d1r = 2 * (4 * weight * sr * d1r + d2r * d2r)
            # Set steps
            if c0 < c2:
                sc = 1
            else:
                sc = -1
            if r0 < r2:
                sr = 1
            else:
                sr = -1
            rc = -2 * sc * sr * (2 * weight * rc + d2c * d2r)

            if cur * sc * sr < 0:
                d1c = -d1c
                d1r = -d1r
                rc = -rc
                cur = -cur

            d2c = 4 * weight * (c1 - c0) * sr * cur + d1c / 2 + rc
            d2r = 4 * weight * (r0 - r1) * sc * cur + d1r / 2 + rc

            # Flat ellipse, algo fails
            if weight < 0.5 and (d2r > rc or d2c < rc):
                cur = (weight + 1) / 2
                weight = np.sqrt(weight)
                rc = 1. / (weight + 1)
                # Subdivide curve in half
                sc = np.floor((c0 + 2 * weight * c1 + c2) * rc * 0.5 + 0.5)
                sr = np.floor((r0 + 2 * weight * r1 + r2) * rc * 0.5 + 0.5)
                d2c = np.floor((weight * c1 + c0) * rc + 0.5)
                d2r = np.floor((r1 * weight + r0) * rc + 0.5)
                return Drawing._bezier_segment(r0, c0, d2r, d2c, sr, sc, cur)

            err = d2c + d2r - rc
            while d2r <= rc and d2c >= rc:
                cc.append(c0)
                rr.append(r0)
                if c0 == c2 and r0 == r2:
                    # The job is done!
                    return np.array(rr, dtype=np.intp), np.array(cc, dtype=np.intp)

                # Save boolean values
                test1 = 2 * err > d2r
                test2 = 2 * (err + d1r) < -d2r
                # Move (c0, r0) to the next position
                if 2 * err < d2c or test2:
                    r0 += sr
                    d2r += rc
                    d2c += d1c
                    err += d2c
                if 2 * err > d2c or test1:
                    c0 += sc
                    d2c += rc
                    d2r += d1r
                    err += d2r

        # Plot line
        cc_t, rr_t = Drawing._line(c0, r0, c2, r2, shape)
        cc.extend(cc_t)
        rr.extend(rr_t)

        return np.array(rr, dtype=np.intp), np.array(cc, dtype=np.intp)

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