(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define location-concept-1
  (def-concept :name "" :is_slot True :parent_space location-space))
(define location-concept-2
  (def-concept :name "" :is_slot True :parent_space location-space))
(define time-concept-1
  (def-concept :name "" :is_slot True :parent_space time-space))
(define time-concept-2
  (def-concept :name "" :is_slot True :parent_space time-space))
(define label-parent-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space
    :locations (list (Location (list) conceptual-space))))
(define relation-parent-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :locations (list (Location (list) more-less-space))))
(def-relation :start label-parent-concept :end relation-parent-concept
  :parent_concept more-concept)
(define time-relation-concept
  (def-concept :name "" :is_slot True :parent_space same-different-space
    :possible_instances (StructureSet same-concept different-concept)))
(define location-relation-concept
  (def-concept :name "" :is_slot True :parent_space same-different-space
    :possible_instances (StructureSet same-concept different-concept)))

(define rp-sub-frame-input
  (def-contextual-space :name "rp-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space conceptual-space)))
(define rp-sub-frame-output
  (def-contextual-space :name "rp-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space conceptual-space)))
(define rp-sub-frame
  (def-sub-frame :name "s-comparative-rp-sub" :parent_concept rp-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet label-parent-concept relation-parent-concept)
    :input_space rp-sub-frame-input
    :output_space rp-sub-frame-output))

(define location-1-sub-frame-input
  (def-contextual-space :name "location-1-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space conceptual-space)))
(define location-1-sub-frame-output
  (def-contextual-space :name "location-1-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space conceptual-space)))
(define location-1-sub-frame
  (def-sub-frame :name "s-comparative-location-1-sub"
    :parent_concept pp-inessive-location-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet location-concept-1)
    :input_space location-1-sub-frame-input
    :output_space location-1-sub-frame-output))

(define location-2-sub-frame-input
  (def-contextual-space :name "location-2-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space conceptual-space)))
(define location-2-sub-frame-output
  (def-contextual-space :name "location-2-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space conceptual-space)))
(define location-2-sub-frame
  (def-sub-frame :name "s-comparative-location-2-sub"
    :parent_concept pp-inessive-location-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet location-concept-2)
    :input_space location-2-sub-frame-input
    :output_space location-2-sub-frame-output))

(define time-1-sub-frame-input
  (def-contextual-space :name "time-1-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet time-space)))
(define time-1-sub-frame-output
  (def-contextual-space :name "time-1-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet string-space grammar-space time-space)))
(define time-1-sub-frame
  (def-sub-frame :name "s-comparative-time-1-sub"
    :parent_concept pp-inessive-time-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet time-concept-1)
    :input_space time-1-sub-frame-input
    :output_space time-1-sub-frame-output))

(define time-2-sub-frame-input
  (def-contextual-space :name "time-2-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet time-space)))
(define time-2-sub-frame-output
  (def-contextual-space :name "time-2-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet string-space grammar-space time-space)))
(define time-2-sub-frame
  (def-sub-frame :name "s-comparative-time-2-sub"
    :parent_concept pp-inessive-time-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet time-concept-2)
    :input_space time-2-sub-frame-input
    :output_space time-2-sub-frame-output))

(define comparative-sentence-input
  (def-contextual-space :name "s-comparative.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space conceptual-space)))
(define comparative-sentence-output
  (def-contextual-space :name "s-comparative.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space conceptual-space)))
(define comparative-sentence
  (def-frame :name "s-comparative" :parent_concept sentence-concept :parent_frame None
    :depth 6
    :sub_frames (StructureSet rp-sub-frame
			      location-1-sub-frame location-2-sub-frame
			      time-1-sub-frame time-2-sub-frame)
    :concepts (StructureSet
	       label-parent-concept relation-parent-concept
	       location-concept-1 location-concept-2
	       time-concept-1 time-concept-2
	       location-relation-concept time-relation-concept)
    :input_space comparative-sentence-input
    :output_space comparative-sentence-output))

(define chunk-start
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) conceptual-space)
			      (Location (list) location-1-sub-frame-input)
			      (Location (list) time-1-sub-frame-input)
			      (Location (list) rp-sub-frame-input)
			      (Location (list) comparative-sentence-input))
    :parent_space location-1-sub-frame-input))
(define chunk-end
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) conceptual-space)
			      (Location (list) location-2-sub-frame-input)
			      (Location (list) time-2-sub-frame-input)
			      (Location (list) rp-sub-frame-input)
			      (Location (list) comparative-sentence-input))
    :parent_space location-2-sub-frame-input))
(define chunk-start-conceptual-label
  (def-label :start chunk-start :parent_concept label-parent-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) rp-sub-frame-input)
		     (Location (list) comparative-sentence-input))
    :parent_space rp-sub-frame-input))
(define chunk-start-location-label
  (def-label :start chunk-start :parent_concept location-concept-1
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) location-1-sub-frame-input)
		     (Location (list) comparative-sentence-input))
    :parent_space location-1-sub-frame-input))
(define chunk-end-location-label
  (def-label :start chunk-end :parent_concept location-concept-2
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) location-2-sub-frame-input)
		     (Location (list) comparative-sentence-input))
    :parent_space location-2-sub-frame-input))
(define chunk-start-time-label
  (def-label :start chunk-start :parent_concept time-concept-1
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) time-1-sub-frame-input)
		     (Location (list) comparative-sentence-input))
    :parent_space time-1-sub-frame-input))
(define chunk-end-time-label
  (def-label :start chunk-end :parent_concept time-concept-2
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) time-2-sub-frame-input)
		     (Location (list) comparative-sentence-input))
    :parent_space time-2-sub-frame-input))

(define time-relation
  (def-relation :start chunk-start :end chunk-end :parent_concept time-relation-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) comparative-sentence-input))
    :parent_space comparative-sentence-input
    :conceptual_space time-space))
(define location-relation
  (def-relation :start chunk-start :end chunk-end :parent_concept location-relation-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan Nan)) (list (list Nan Nan)) location-space)
		     (TwoPointLocation (list) (list) comparative-sentence-input))
    :parent_space comparative-sentence-input
    :conceptual_space location-space))

(define relation
  (def-relation :start chunk-start :end chunk-end :parent_concept relation-parent-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list) (list) conceptual-space)
		     (TwoPointLocation (list) (list) rp-sub-frame-input)
		     (TwoPointLocation (list) (list) comparative-sentence-input))
    :parent_space rp-sub-frame-input
    :conceptual_space conceptual-space))

(define sentence-word-1
  (def-letter-chunk :name "temperatures"
    :locations (list nsubj-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-1-label
  (def-label :start sentence-word-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) comparative-sentence-output))))
(define sentence-word-2
  (def-letter-chunk :name "will"
    :locations (list vb-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk will))
(define sentence-word-3
  (def-letter-chunk :name "be"
    :locations (list cop-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk be))
(define sentence-word-4
  (def-letter-chunk :name None
    :locations (list rp-location
		     (Location (list) rp-sub-frame-output)
		     (Location (list) comparative-sentence-output))
    :parent_space rp-sub-frame-output))
(define jjr-chunk-grammar-label
  (def-label :start sentence-word-4 :parent_concept rp-concept
    :locations (list rp-location
		     (Location (list) rp-sub-frame-output))))
(define sentence-word-5
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) location-1-sub-frame-output)
		     (Location (list) comparative-sentence-output))
    :parent_space location-1-sub-frame-output))
(define location-chunk-grammar-label
  (def-label :start sentence-word-5 :parent_concept pp-inessive-location-concept
    :locations (list pp-location
		     (Location (list) location-1-sub-frame-output))))
(define sentence-word-6
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) time-1-sub-frame-output)
		     (Location (list) comparative-sentence-output))
    :parent_space time-1-sub-frame-output))
(define sentence-word-7
  (def-letter-chunk :name "than"
    :locations (list prep-location
		     (Location (list) comparative-sentence-output))
    :abstract_chunk than))
(define sentence-word-8
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) location-2-sub-frame-output)
		     (Location (list) comparative-sentence-output))
    :parent_space location-2-sub-frame-output))
(define location-chunk-grammar-label
  (def-label :start sentence-word-8 :parent_concept pp-inessive-location-concept
    :locations (list pp-location
		     (Location (list) location-2-sub-frame-output))))
(define sentence-word-9
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) time-2-sub-frame-output)
		     (Location (list) comparative-sentence-output))
    :parent_space time-2-sub-frame-output))

(define v-super-chunk
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-2)
    :right_branch (StructureSet sentence-word-3)))
(define v-super-chunk-label
  (def-label :start v-super-chunk :parent_concept v-concept
    :locations (list v-location
		     (Location (list) comparative-sentence-output))))
(define pp-1-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-5)
    :right_branch (StructureSet sentence-word-6)))
(define pp-1-super-chunk-label
  (def-label :start pp-1-super-chunk :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) comparative-sentence-output))))
(define pp-2-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-8)
    :right_branch (StructureSet sentence-word-9)))
(define pp-2-super-chunk-label
  (def-label :start pp-2-super-chunk :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) comparative-sentence-output))))
(define comparative-super-chunk
  (def-letter-chunk :name None
    :locations (list rp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-7)
    :right_branch (StructureSet pp-2-super-chunk)))
(define comparative-super-super-chunk
  (def-letter-chunk :name None
    :locations (list rp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet pp-1-super-chunk)
    :right_branch (StructureSet comparative-super-chunk)))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-4)
    :right_branch (StructureSet comparative-super-super-chunk)))
(define pred-super-chunk-label
  (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) comparative-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet v-super-chunk)
    :right_branch (StructureSet pred-super-chunk)))
(define vp-super-chunk-label
  (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) comparative-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-1)
    :right_branch (StructureSet vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) comparative-sentence-output))))

(def-relation :start rp-concept :end comparative-sentence
  :is_bidirectional True :stable_activation 0.6)
(def-relation :start pp-inessive-location-concept :end comparative-sentence
  :is_bidirectional True :stable_activation 0.2)
(def-relation :start pp-inessive-time-concept :end comparative-sentence
  :is_bidirectional True :stable_activation 0.2)
