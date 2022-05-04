(define label-parent-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define nn-input
  (def-contextual-space :name "np[nn].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space)))
(define nn-output
  (def-contextual-space :name "np[nn].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space)))
(define nn-frame
  (def-frame :name "np[nn]"
    :parent_concept np-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection label-parent-concept)
    :input_space nn-input :output_space nn-output))
(define chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) nn-input))
    :parent_space nn-input))
(define chunk-label
  (def-label :start chunk :parent_concept label-parent-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-input))))
(define letter-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan Nan)) location-space)
		     nn-location
		     (Location (list) nn-output))
    :parent_space nn-output))
(define letter-chunk-grammar-label
  (def-label :start letter-chunk :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) nn-output))))
(define letter-chunk-meaning-label
  (def-label :start letter-chunk :parent_concept label-parent-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-output))))
(define null-chunk
  (def-letter-chunk :name ""
    :locations (list null-location
		     (Location (list) nn-output))
    :parent_space nn-output))
(define np-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) nn-output))
    :parent_space nn-output
    :left_branch (StructureCollection letter-chunk)
    :right_branch (StructureCollection null-chunk)))
(define np-super-chunk-label
  (def-label :start np-super-chunk :parent_concept np-concept
    :locations (list np-location
		     (Location (list) nn-output))))
   
(def-relation :start label-concept :end nn-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end nn-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end nn-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start nn-concept :end nn-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start np-concept :end nn-frame
  :is_bidirectional True :activation 1.0)
