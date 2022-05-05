(load "conceptual-spaces/grammar.lisp")
(load "conceptual-spaces/sameness.lisp")
(load "conceptual-spaces/more-less.lisp")
(load "conceptual-spaces/magnitude.lisp")
(load "conceptual-spaces/height.lisp")
(load "conceptual-spaces/goodness.lisp")
(load "conceptual-spaces/lateness.lisp")
(load "conceptual-spaces/extremeness.lisp")
(load "conceptual-spaces/temperature.lisp")
(load "conceptual-spaces/peripheralness.lisp")
(load "conceptual-spaces/location.lisp")
(load "conceptual-spaces/time.lisp")

(load "frames/ap-jj.lisp")
(load "frames/np-nn.lisp")
(load "frames/rp-jjr.lisp")
(load "frames/s-ap-in-np.lisp")
(load "frames/s-comparative.lisp")
(load "frames/s-and.lisp")

(define input-space
  (def-contextual-space :name "input" :parent_concept input-concept
    :conceptual_spaces (StructureCollection temperature-space location-space)
    :is_main_input True))

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 2)) temperature-space)
		   (Location (list (list 0 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 0 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 19)) temperature-space)
		   (Location (list (list 0 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 0 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 7)) temperature-space)
		   (Location (list (list 2 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 8)) temperature-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 2 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 2 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 4 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 15)) temperature-space)
		   (Location (list (list 4 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 4 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list -2)) temperature-space)
		   (Location (list (list 6 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list -2)) temperature-space)
		   (Location (list (list 6 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 9)) temperature-space)
		   (Location (list (list 6 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 14)) temperature-space)
		   (Location (list (list 6 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 1)) temperature-space)
		   (Location (list (list 6 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 9)) temperature-space)
		   (Location (list (list 8 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 8 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 8 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 30)) temperature-space)
		   (Location (list (list 8 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 27)) temperature-space)
		   (Location (list (list 8 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 18)) temperature-space)
		   (Location (list (list 10 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 13)) temperature-space)
		   (Location (list (list 10 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 10 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 25)) temperature-space)
		   (Location (list (list 10 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 10 8)) location-space))
  :parent_space input-space)

