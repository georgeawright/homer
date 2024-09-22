(load "narration-kb.lisp")

(define monday-concept
  (def-concept :name "monday" :locations (list (Location (list (list 72)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))

(define monday-word
  (def-letter-chunk :name "monday" :parent_space time-space
    :locations (list nn-location (Location (list (list 72)) time-space))))
(def-relation :start monday-concept :end monday-word :parent_concept nn-concept)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 3)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 1 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 1 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 1 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 1 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 3 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 3 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 3 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 3 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 5 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 5 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 5 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 5 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 7 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 7 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 7 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 7 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 1 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 1 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 1 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 1 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 7)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 3 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 3 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 3 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 3 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 8)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 5 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 5 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 7)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 5 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 5 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 7)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 7 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 8)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 7 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 7)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 7 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 7)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 7 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 1 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 1 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 1 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 1 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 3 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 3 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 3 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 3 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 5 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 5 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 5 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 5 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 7 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 7 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 7 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 7 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 1 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 1 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 1 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 1 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 3 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 3 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 3 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 3 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 5 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 5 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 5 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 5 7)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 7 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 7 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 7 5)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 72)) time-space)
		   (Location (list (list 7 7)) location-space))
  :parent_space input-space)
