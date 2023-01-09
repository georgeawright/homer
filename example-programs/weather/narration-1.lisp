(load "conceptual-spaces/grammar.lisp")
(load "conceptual-spaces/negativeness.lisp")
(load "conceptual-spaces/more-less.lisp")
(load "conceptual-spaces/same-different.lisp")
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

(load "frames/pp-between-times.lisp")

(load "frames/pp-inessive-location.lisp")
(load "frames/pp-from-to-different-locations.lisp")
(load "frames/pp-from-wards-locations.lisp")

(load "frames/s-be.lisp")
(load "frames/s-increase.lisp")
(load "frames/s-move.lisp")
(load "frames/s-spread.lisp")
(load "frames/s-expand.lisp")

(load "frames/s-and.lisp")
(load "frames/s-then.lisp")

(define input-space
  (def-contextual-space
    :name "input" :parent_concept input-concept :is_main_input True
    :conceptual_spaces (StructureSet
			temperature-space location-space time-space)))

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

