class ROIExtractor:

    @staticmethod
    def get_eye_rois(face):

        x, y, w, h = face

        # Left Eye ROI
        left_x = x + int(w * 0.15)
        left_y = y + int(h * 0.25)
        left_w = int(w * 0.25)
        left_h = int(h * 0.20)

        # Right Eye ROI
        right_x = x + int(w * 0.60)
        right_y = y + int(h * 0.25)
        right_w = int(w * 0.25)
        right_h = int(h * 0.20)

        return (
            (left_x, left_y, left_w, left_h),
            (right_x, right_y, right_w, right_h)
        )