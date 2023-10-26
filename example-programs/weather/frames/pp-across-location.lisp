(define location-label-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define size-label-concept
  (def-concept :name "" :is_slot True :parent_space size-space
    :possible_instances (StructureSet medium-concept large-concept)))

(define pp-across-location-input
  (def-contextual-space :name "pp[across-location].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space)))
(define pp-across-location-output
  (def-contextual-space :name "pp[across-location].text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space location-space)))
(define pp-across-location
  (def-frame :name "pp[across-location]"
    :parent_concept pp-inessive-location-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet location-label-concept size-label-concept)
    :input_space pp-across-location-input
    :output_space pp-across-location-output))

(define chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) pp-across-location-input))
    :parent_space pp-across-location-input))
(define chunk-location-label
  (def-label :start chunk :parent_concept location-label-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-across-location-input))
    :parent_space pp-across-location-input))
(define chunk-size-label
  (def-label :start chunk :parent_concept size-label-concept
    :locations (list (Location (list (list Nan)) size-space)
		     (Location (list) pp-across-location-input))
    :parent_space pp-across-location-input))

(define pp-word-1
  (def-letter-chunk :name "across"
    :locations (list prep-location
		     (Location (list) pp-across-location-output))
    :parent_space pp-across-location-output
    :abstract_chunk across))
(define pp-word-2
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) pp-across-location-output))
    :parent_space pp-across-location-output
    :abstract_chunk the))
(define pp-word-3
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-across-location-output))
    :parent_space pp-across-location-output))
(define pp-word-3-grammar-label
  (def-label :start pp-word-3 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-across-location-output))))
(define pp-word-3-meaning-label
  (def-label :start pp-word-3 :parent_concept location-label-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-across-location-output))))

(define np-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) pp-across-location-output))
    :parent_space pp-across-location-output
    :left_branch (StructureSet pp-word-2)
    :right_branch (StructureSet pp-word-3)))
(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-across-location-output))
    :parent_space pp-across-location-output
    :left_branch (StructureSet pp-word-1)
    :right_branch (StructureSet np-super-chunk)))
(define pp-super-chunk-label
  (def-label :start pp-super-chunk :parent_concept pp-inessive-location-concept
    :locations (list pp-location
		     (Location (list) pp-across-location-output))))

(def-relation :start location-concept :end pp-across-location
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start medium-concept :end pp-across-location
  :is_bidirectional True :stable_activation 0.5)

