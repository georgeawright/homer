(load "conceptual-spaces/grammar.lisp")
(load "conceptual-spaces/same-different.lisp")
(load "conceptual-spaces/more-less.lisp")
(load "conceptual-spaces/magnitude.lisp")
(load "conceptual-spaces/height.lisp")
(load "conceptual-spaces/goodness.lisp")
(load "conceptual-spaces/size.lisp")
(load "conceptual-spaces/lateness.lisp")
(load "conceptual-spaces/extremeness.lisp")
(load "conceptual-spaces/temperature.lisp")
(load "conceptual-spaces/peripheralness.lisp")
(load "conceptual-spaces/location.lisp")
(load "conceptual-spaces/time.lisp")

(load "frames/ap-jj.lisp")

(load "frames/pp-from-to-different-locations.lisp")
(load "frames/pp-between-times.lisp")

(load "frames/s-move.lisp")

(define input-space
  (def-contextual-space
    :name "input" :parent_concept input-concept :is_main_input True
    :conceptual_spaces (StructureCollection
			temperature-space location-space time-space)))

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 8)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 8)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 8)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 2 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 9)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 2 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 9)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 4 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 4 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 21)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 6 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 6 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 6 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 6 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 8 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 8 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 8 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 8 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 2 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 2 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 21)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 4 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 4 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 13)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 6 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 24)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 6 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 6 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 6 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 14)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 8 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 13)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 8 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 13)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 8 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 8 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 20)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 2 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 20)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 2 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 14)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 21)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 4 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 20)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 4 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 6 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 14)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 6 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 14)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 6 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 6 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 8 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 8 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 8 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 8 8)) location-space))
  :parent_space input-space)

